# Import Shadow

Find local Python modules or regular packages whose top-level names collide
with a fixed catalog of common standard-library names. Link each candidate to
absolute import sites, including aliases, dotted imports and from-imports.
This helps a worker investigate an accidental `json.py` or `logging/` before
trusting a familiar import spelling. Source is parsed, never executed.

Run from the repository root with Python 3.9 or newer, offline:

```sh
python3 -B line-3/tools/import-shadow/shadow.py line-3/tools/import-shadow/examples
```

When tried, this exited 0 and found `json/__init__.py` with three absolute
import sites. The relative import was excluded. Both top-level execution traps
remained unexecuted. Ten behavioral tests passed:

```sh
python3 -B -m unittest discover -s line-3/tools/import-shadow -v
```

The actual `shared/import-drift` worker was also inspected as source only:
34 files, 170,606 bytes, no name collisions, namespace-only matches or parse
issues. [observed-source.json](observed-source.json) retains the byte manifest
and complete result. This negative result is limited to the admitted sources
and named catalog; it does not establish runtime isolation.

`--json` gives paths, source coordinates (AST UTF-8 byte columns), alias indexes,
the full name catalog, source SHA-256 manifest, collection limits and issues.
Repeated from-list names retain separate sites. All syntactic scopes are
inspected, including unreachable branches. `--strict` exits 1 if there are
regular candidates or parse/module-collision issues; namespace-only candidates
alone do not trigger it. Ordinary completion exits 0. Invalid catalogs,
collection failures and exhausted budgets exit 2 with a structured refusal and
no partial analysis.

The default catalog is an explicit portable subset, independent of installed
packages or machine library paths. `--names requests,flask` replaces it with
an explicit comma-separated catalog for another review. Names must be top-level
Python identifiers. No package discovery, installation or library import probe
is performed. Built-in or frozen names such as `sys` and `os` remain *name
collision* candidates; their presence does not mean a local file can override
the interpreter's preferred module.

Only top-level `.py` files and regular packages are collision candidates.
`pkg/json.py` does not shadow absolute `json` for the declared root. A namespace
`json/` without `__init__.py` is listed separately: a regular package elsewhere
can win over namespace portions. A package wins a same-named `.py` collision,
with both source paths retained and the shadowed source left unparsed, matching
Import Map. Root-level `__init__.py` has no inferred module name. Relative
imports and dynamic calls are excluded from linked absolute sites. Parse
failures may hide import sites.

This reuses the delivered Import Budget collector and Import Map naming rules
without changing either. Default budgets: 1,000 files, 262,144 bytes per file,
8,388,608 total source bytes, 20,000 directory entries, depth 64. Override with
`--max-files`, `--max-file-bytes`, `--max-total-bytes`, `--max-entries`,
`--max-depth`. Roots must be inside the current workspace; symlinks, hidden
and conventional dependency directories are skipped. Keep sources stable during
collection. These are input limits, not a CPU or time guarantee.

Static candidates do not establish runtime resolution, a vulnerability or an
import failure. Search path order, caches, built-in/frozen precedence, custom
loaders, extension modules and runtime bindings remain unknown. No automatic
rename or source edit is attempted. No coin, wallet or network is needed.
