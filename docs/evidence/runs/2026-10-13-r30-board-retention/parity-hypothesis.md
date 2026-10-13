# Superseded parity hypothesis

The independent proposed even-backslash table-width defect was a false positive.
The captured `parity-red.json` expects ordinary inline Markdown escape parity;
that expectation does not match GFM table-cell scanning. It is preserved as a
failed hypothesis, not evidence of a production defect.

The official cmark-gfm scanner at commit
`27d942c8b0a62d192f616e5bf3578f4b6a89e180` consumes a pipe immediately preceded
by a backslash for runs of one, two, three and four backslashes.
[gfm-scanner.json](gfm-scanner.json) pins the source URL/hash and actual compiled
scanner output; [gfm-scanner-probe.c](gfm-scanner-probe.c) is the focused caller.
Compile the exact referenced ext_scanners.c with its bufsize_t typedef and this
caller. Length4 for zero slashes stops before the first pipe; lengths11–14 for
1–4 slashes consume it and stop before the next unescaped pipe.

The proposed regex change and its four misleading parity controls were removed
before commit. The production validator is byte-identical to accepted f974e7f.
The six actual owner-process controls remain those frozen at4aa28e1.
This is scanner evidence, not a claim to implement all Markdown semantics.
