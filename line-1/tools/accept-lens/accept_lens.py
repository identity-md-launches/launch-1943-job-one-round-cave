#!/usr/bin/env python3
"""Compare two bounded, anonymous HTTP content negotiations."""

import argparse
import datetime as dt
import hashlib
import http.client
import ipaddress
import json
import math
import ssl
import subprocess
import sys
import time
import urllib.parse

USER_AGENT = "Pepeolithic-Accept-Lens/1.0 (read-only diagnostics)"
ACCEPTS = (("json", "application/json"), ("html", "text/html"))


def validate_url(value):
    if not isinstance(value, str) or any(ord(c) <= 32 or ord(c) == 127 for c in value):
        raise ValueError("URL must contain no whitespace or control characters")
    value.encode("ascii")
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username is not None or parsed.password is not None:
        raise ValueError("use an absolute HTTPS URL without credentials")
    if parsed.fragment:
        raise ValueError("remove URL fragment")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError("invalid port")
    host = parsed.hostname
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        if host == "localhost" or host.endswith(".local"):
            raise ValueError("use a public host")
    else:
        if not address.is_global:
            raise ValueError("use a public host")
    return parsed


def strict_json(body):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate JSON key")
            out[key] = value
        return out

    def finite(text):
        number = float(text)
        if not math.isfinite(number):
            raise ValueError("non-finite JSON number")
        return number

    return json.loads(body.decode("utf-8-sig"), object_pairs_hook=unique,
                      parse_float=finite, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("non-JSON constant")))


def observe(url, accept, max_bytes, timeout, factory=None):
    parsed = validate_url(url)
    started = time.monotonic()
    result = {"accept": accept}
    connection = None
    try:
        connection = (factory or http.client.HTTPSConnection)(
            parsed.hostname, parsed.port or 443, timeout=timeout,
            context=ssl.create_default_context())
        target = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
        connection.request("GET", target, headers={
            "User-Agent": USER_AGENT, "Accept": accept,
            "Accept-Encoding": "identity", "Connection": "close"})
        response = connection.getresponse()
        content_type = response.getheader("Content-Type", "")
        encoding = response.getheader("Content-Encoding", "identity")
        result.update(status=response.status,
                      media_type=content_type.split(";", 1)[0].strip().lower(),
                      content_encoding=encoding.lower(),
                      redirect_location_present=bool(response.getheader("Location")))
        if encoding.lower() not in ("", "identity"):
            raise ValueError("server returned compressed body despite identity request")
        body = bytearray()
        while len(body) <= max_bytes:
            if connection.sock is not None:
                remaining = timeout - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("sample deadline exceeded")
                connection.sock.settimeout(remaining)
            chunk = response.read1(min(65536, max_bytes + 1 - len(body)))
            if not chunk:
                break
            body.extend(chunk)
        result["body_bytes"] = len(body)
        if len(body) > max_bytes:
            raise ValueError("response exceeds byte limit")
        result["body_sha256"] = hashlib.sha256(body).hexdigest()
        try:
            strict_json(body)
        except (ValueError, UnicodeError, RecursionError):
            result["valid_json"] = False
        else:
            result["valid_json"] = True
        result["ok"] = True
    except (OSError, ValueError, http.client.HTTPException, UnicodeError) as error:
        result.update(ok=False, error={"kind": type(error).__name__, "message": str(error)})
    finally:
        if connection is not None:
            connection.close()
    result["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
    return result


def compare(samples):
    if len(samples) != 2 or any(not isinstance(s, dict) for s in samples):
        raise ValueError("two samples required")
    if not all(s.get("ok") is True for s in samples):
        return {"verdict": "incomplete", "differences": []}
    left, right = samples
    fields = ("status", "media_type", "content_encoding", "valid_json", "redirect_location_present")
    differences = [field for field in fields if left[field] != right[field]]
    return {"verdict": "negotiation_changed" if differences else "same_observed_contract",
            "differences": differences,
            "body_digests_differ": left["body_sha256"] != right["body_sha256"]}


def run(url, deadline, max_bytes, runner=None):
    validate_url(url)
    start = time.monotonic()
    samples = []
    for _, accept in ACCEPTS:
        remaining = deadline - (time.monotonic() - start)
        if remaining <= 0:
            samples.append({"accept": accept, "ok": False,
                            "error": {"kind": "deadline", "message": "total deadline elapsed"}})
            continue
        command = [sys.executable, "-I", "-B", __file__, "--worker", url, accept,
                   str(max_bytes), str(remaining)]
        try:
            process = (runner or subprocess.run)(command, capture_output=True, text=True,
                                                  timeout=remaining, env={})
            if process.returncode != 0:
                raise ValueError("sample worker exited without a valid report")
            sample = json.loads(process.stdout)
            if not isinstance(sample, dict) or sample.get("accept") != accept or type(sample.get("ok")) is not bool:
                raise ValueError("invalid sample worker report")
        except subprocess.TimeoutExpired:
            sample = {"accept": accept, "ok": False,
                      "error": {"kind": "deadline", "message": "sample worker timed out"}}
        except (OSError, ValueError, UnicodeError):
            sample = {"accept": accept, "ok": False,
                      "error": {"kind": "worker", "message": "invalid sample worker report"}}
        samples.append(sample)
    return {"schema": "accept-lens/v1", "url": url,
            "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "limits": {"deadline_seconds": deadline, "max_bytes_per_sample": max_bytes},
            "samples": samples, "comparison": compare(samples),
            "elapsed_ms": round((time.monotonic() - start) * 1000, 3)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("url", help="public, non-secret HTTPS GET endpoint")
    parser.add_argument("--deadline", type=float, default=10)
    parser.add_argument("--max-bytes", type=int, default=262144)
    args = parser.parse_args(argv)
    try:
        validate_url(args.url)
        if not math.isfinite(args.deadline) or not 0 < args.deadline <= 30:
            raise ValueError("deadline must be greater than zero and at most 30 seconds")
        if not 1 <= args.max_bytes <= 1048576:
            raise ValueError("max-bytes must be between 1 and 1048576")
    except (ValueError, UnicodeError) as error:
        parser.error(str(error))
    result = run(args.url, args.deadline, args.max_bytes)
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["comparison"]["verdict"] != "incomplete" else 1


if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[1] == "--worker":
        print(json.dumps(observe(sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]))))
    else:
        sys.exit(main())
