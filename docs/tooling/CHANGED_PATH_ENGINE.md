# Canonical changed-path engine

`logos_validation.changed_paths` is the single additive engine for identifying
Git changes by layer. T498 lands the engine and its output contract only. No
existing validator, hook, workflow, or CI job consumes it yet.

## Profiles and layers

The engine always reports four independently computed layers:

- `committed`: merge-base to `HEAD`;
- `staged`: merge-base to the index, never stale `HEAD` to the index;
- `unstaged`: index to worktree;
- `untracked`: standard non-ignored untracked files.

Named profiles select the union: `ci` uses committed; `pre-commit` uses
committed and staged; `task-scope` and `local-full` use all four. A task-scope
caller may pass repeatable `--scope` rules to classify unrelated dirty paths.

## CLI

```powershell
python -m logos_validation.changed_paths --profile ci
python -m logos_validation.changed_paths --profile pre-commit
python -m logos_validation.changed_paths --profile task-scope --scope .ai/tasks/T498.task.yaml --scope logos_validation/
```

The default output is the versioned JSON contract in
`schemas/changed-paths-output.schema.json`. `--null-separated` emits the selected
union only after a successful resolution. A failure emits JSON with non-null
`fail`, exits 2, and must never be treated as an empty changed set.

By default the engine fetches the base and resolves a fresh merge-base. Offline
or fixture use must state both `--no-fetch --allow-stale`; the result then records
the stale-base warning. Shallow repositories deepen in bounded 200-commit rounds
and fail with `CP-NO-MERGE-BASE` when ancestry remains unresolved.

`parity_log_line(consumer, legacy_paths, result)` returns one deterministic
JSONL record for later LSG-O2B shadow comparisons. It performs no file write and
does not activate any consumer in this PR.

## Migration and rollback

This PR has no consumers and changes no existing behavior. Later LSG-O2B PRs
must use shadow parity before cutover. Rollback is a direct revert of this
package, schema, documentation, and tests.

The engine reads Git metadata only. It does not read or change Scripture data,
doctrine, graph edges, retrieval, vectors, indexes, or governance authority.
