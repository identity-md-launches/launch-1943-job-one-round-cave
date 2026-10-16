# Read Batch

Prepare ABI-encoded `eth_call` requests and decode saved batch replies offline.
JSON-RPC batches can return replies in any order; this tool pairs them by ID
and keeps each decoded result, RPC error, missing response or decoding failure
beside its original target, block identifier and arguments. This lets an
unfamiliar worker build a small set of reads and review their outputs without
implementing RPC pairing or ABI dispatch themselves.

Run from the repository root with Python 3.10+ and no installed packages:

```sh
python3 -B line-4/tools/read-batch/read_batch.py demo
```

Tried: exit 0. It prepared ZTO `totalSupply()` with selector `0x18160ddd`,
checked exact equality with the inherited saved request at block `0x18fd343`,
then decoded the inherited response as raw uint256
`1000000000000000000000000000`. This is historical provider evidence retained
by [Transcript Inspector](../transcript-inspector/README.md), not a fresh query,
current supply, verified contract ABI or state proof. No token decimal count is
assumed. ZTO is the first token example; this works for IMD and other targets
when the worker supplies their ABI, address and arguments.

Prepare the delivered historical example:

```sh
python3 -B line-4/tools/read-batch/read_batch.py prepare --abi line-4/tools/transcript-inspector/zto-total-supply-abi.json --spec line-4/tools/read-batch/zto-spec.json
```

Tried: exit 0, the same request as the retained `zto-plan.json`. The input
specification has exactly `block` and `calls`. Each call has exactly `id`,
`to`, `function` and `args`, as illustrated in `zto-spec.json`. Add more calls
to that array for a batch. `function` requires an explicit signature; supported
aliases are canonicalized. `args` must be a JSON array. All targets and values
are supplied explicitly. No owner, recipient or account address is invented.
Selected functions must explicitly declare `view` or `pure`; input selector
collisions and duplicate matching signatures are refused before producing a plan.

The output has `schema: read-batch-plan/v1` and a `requests` array. That array
is the JSON-RPC batch payload a person can separately review and send through
their own client. The enclosing plan object is local metadata, not an RPC
payload. This program has no network client and sends nothing.

Review a saved response array against that plan:

```sh
python3 -B line-4/tools/read-batch/read_batch.py inspect --abi line-4/tools/transcript-inspector/zto-total-supply-abi.json --plan line-4/tools/read-batch/zto-plan.json --responses line-4/tools/read-batch/zto-responses.json
```

Tried: exit 0 and the historical ZTO value above. The response file is a JSON
array, even for one request. Replies may be shuffled. Integer `3` and string
`"3"` are distinct IDs. Duplicate IDs, unknown response IDs, notifications,
null/bool/float IDs, malformed envelopes and extra request fields are refused.
An absent response remains visible as `missing-response`; it is never inferred
from a neighboring reply. Valid RPC errors and noncanonical return data yield
individual findings without hiding good results from other calls. A
batch-level error object must be handled by the user's client, not interpreted
as an array of replies.

Exit 0 means all present planned calls decoded (or preparation succeeded).
Exit 1 means the review contains missing responses, RPC errors or unresolved
calls/return data. Exit 2 means invalid input, with a concise stderr error and
no JSON report. Results preserve request order and include each call's block
identifier. Different numeric blocks may be reviewed; block tags can resolve
to different states even within a batch. This is not an atomic multicall.

Bounds: 1..32 requests, 0..32 saved replies, IDs of up to 128 characters or
integers with absolute value at most 2^53−1, and separate aggregate calldata
and return-data limits of 512 KiB each. Block identifiers are explicit tags or
canonical hex quantities of at most 256 bits. Explicit JSON input files must
resolve inside the current workspace; plans, specs and responses are capped
at 2 MiB each, ABIs at 1 MiB, and duplicate object fields are rejected. At most
256 ABI functions and the existing codec's supported-type and nesting limits
apply. These are structural limits, not precise CPU or memory guarantees.

Reuses sibling Transcript Inspector, Call Inspector, Selector Audit and ABI
Workbench; retain those folders. All selected return schemas are admitted even
when their responses are missing. Strict re-encoding rejects surplus or
noncanonical return bytes. Unsupported input schemas fail closed so a skipped
signature cannot conceal a selector collision. Unselected output schemas are
not interpreted. Arguments must be ABI values in raw units; token decimal
conversion is outside this tool.

The ABI and saved plan/replies are untrusted evidence. A declared `view`
function does not prove deployed behavior, target identity, chain identity,
freshness, ABI completeness or truth of a saved response. Keep the same ABI
when preparing and interpreting a plan: the plan does not embed or authenticate
it. No key, wallet, environment-variable read, signing, transaction submission,
payment, posting or deployment is involved.

Sixteen focused behavioral tests passed, including shuffled typed IDs,
independent ABI words/selectors, collisions, partial and failed batches,
canonical return checks, refusal boundaries, CLI statuses and the retained
real ZTO request/response:

```sh
python3 -B -m unittest discover -s line-4/tools/read-batch -v
```

The dependency suites were also run; commands and results are retained in
`line-4/checks39.json`. Only offline fixtures were used this round.
