# T440 DAD Preflight

Task: T440.
Mode: source-specific parser contract, non-authorizing.

DAD lessons checked from the T431-T439 Rust rollout loop:

- source views must be filtered and checksum-traced before scanners consume them;
- package-level metadata is not local row authority;
- field-name overlap such as lemma, morph, Strong, witness, or variant needs semantic policy-cover;
- count parity is necessary but not sufficient;
- no-text Python fixtures should define semantics before Rust scales them.

T440 applies those lessons by defining separate UXLC and OSHB Jonah parser contracts. The task closes the source-specific parser-semantics blocker for future T441 design, but it does not add Rust code, create production rows, store visible Hebrew text, select a source tradition, or judge translation faithfulness.

Reusable DAD note if this pattern repeats:

> Before Rust scans a second source family, write a source-specific parser contract that explains each high-authority field name, records negative fixtures, and proves which parity claims are only count/coverage evidence.

DAD is candidate-only and does not override local Scripture Graph authority.
