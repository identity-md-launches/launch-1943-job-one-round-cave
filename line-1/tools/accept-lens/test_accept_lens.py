import importlib.util
from pathlib import Path
import subprocess
import unittest


spec = importlib.util.spec_from_file_location("accept_lens", Path(__file__).with_name("accept_lens.py"))
lens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lens)


class Response:
    status = 200

    def __init__(self, body=b'{"ok":true}', media="application/json"):
        self.body = body
        self.media = media

    def getheader(self, name, default=None):
        return {"Content-Type": self.media}.get(name, default)

    def read1(self, count):
        chunk, self.body = self.body[:count], self.body[count:]
        return chunk


class Connection:
    sock = None

    def __init__(self, response, *args, **kwargs):
        self.response = response
        self.requested = None

    def request(self, method, target, headers):
        self.requested = (method, target, headers)

    def getresponse(self):
        return self.response

    def close(self):
        pass


class AcceptLensTests(unittest.TestCase):
    def test_observe_distinguishes_json_from_html_without_body_leak(self):
        seen = []

        def factory(*args, **kwargs):
            connection = Connection(Response(b"<html>healthy</html>", "text/html; charset=utf-8"))
            seen.append(connection)
            return connection

        report = lens.observe("https://api.imd.fun/launches", "text/html", 100, 1, factory)
        self.assertTrue(report["ok"])
        self.assertEqual(report["media_type"], "text/html")
        self.assertFalse(report["valid_json"])
        self.assertNotIn("healthy", str(report))
        self.assertEqual(seen[0].requested[0:2], ("GET", "/launches"))
        self.assertEqual(seen[0].requested[2]["Accept"], "text/html")

    def test_byte_cap_is_enforced_without_returning_body(self):
        report = lens.observe("https://api.imd.fun/", "application/json", 4, 1,
                              lambda *a, **k: Connection(Response(b"secret body")))
        self.assertFalse(report["ok"])
        self.assertEqual(report["body_bytes"], 5)
        self.assertNotIn("secret", str(report))

    def test_negotiated_contract_changes_and_dynamic_digest_is_informational(self):
        first = {"ok": True, "status": 200, "media_type": "application/json",
                 "content_encoding": "identity", "valid_json": True,
                 "redirect_location_present": False, "body_sha256": "a"}
        second = dict(first, body_sha256="b")
        self.assertEqual(lens.compare([first, second])["verdict"], "same_observed_contract")
        second.update(status=406, media_type="text/html", valid_json=False)
        changed = lens.compare([first, second])
        self.assertEqual(changed["verdict"], "negotiation_changed")
        self.assertEqual(changed["differences"], ["status", "media_type", "valid_json"])

    def test_total_deadline_keeps_missing_sample_explicit(self):
        def timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

        report = lens.run("https://api.imd.fun/launches", 0.5, 64, timeout)
        self.assertEqual(report["comparison"]["verdict"], "incomplete")
        self.assertTrue(all(not item["ok"] for item in report["samples"]))

    def test_rejects_credentials_private_literals_and_fragments(self):
        for url in ("http://api.imd.fun/", "https://user:pass@api.imd.fun/",
                    "https://127.0.0.1/", "https://api.imd.fun/#frag",
                    "https://api.imd.fun:0/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                lens.validate_url(url)


if __name__ == "__main__":
    unittest.main()
