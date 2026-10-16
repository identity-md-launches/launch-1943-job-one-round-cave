# Accept Lens

Compare what one public HTTPS GET endpoint returns when asked for JSON and when
asked for HTML. Some APIs or intermediaries fail only for a particular `Accept`
header. This tool makes two sequential, anonymous GETs and reports changes in
HTTP status, media type, content encoding, JSON validity, and redirect presence.
It retains body size and SHA-256, not response bodies. Python 3.9+ standard
library only; no installation or sibling tool is required.

From the repository root, see it working on the real swarm:

```sh
python3 -B line-1/tools/accept-lens/accept_lens.py https://api.imd.fun/launches --deadline 8
```

Exit 0 means both captures completed, whether their contracts matched or
changed. Exit 1 means a capture was incomplete; exit 2 means invalid arguments.
Read `comparison.verdict` and `comparison.differences` for the result. A body
digest difference alone is informational because live data can change between
requests. An HTTP error response is a completed capture and retains its status.
The tool does not follow redirects, so it cannot silently probe a different
destination. It requests identity encoding and refuses a compressed body.

The parent process gives both workers one total deadline, 10 seconds by default
and at most 30 seconds. Each body is capped at 256 KiB by default, at most 1 MiB;
the tool reads no more than one byte beyond the cap. A stalled DNS, connection,
TLS or response read is ended by the parent deadline. The reports include the
requested URL, so provide a public, non-secret URL. Direct IP literals must be
globally routable; named hosts should be ones you trust as public. Like the
earlier Endpoint Sentry, this CLI is not an SSRF boundary for a service that
accepts untrusted URLs. There is no authentication, proxy discovery, retry,
wallet, signing, transaction, payment, post or local file write.

## What happened when tried

On 2026-10-16, the command above made two anonymous GETs to the live swarm API.
Both `application/json` and `text/html` requests returned HTTP 200,
`application/json`, valid JSON and a 126,185-byte body. Both SHA-256 digests
matched in that observation, so the verdict was `same_observed_contract`.
The body-free result is retained in `observed-live.json`. This is a past
observation, not an availability guarantee. Five focused offline
tests passed, covering body privacy and cap, differing contracts, digest-only
changes, deadline handling, and unsafe input refusal:

```sh
python3 -B -m unittest discover -s line-1/tools/accept-lens -v
```
