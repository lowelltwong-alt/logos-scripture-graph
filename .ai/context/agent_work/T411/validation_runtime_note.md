# T411 Validation Runtime Note

Use the repository's long timeout ceilings for merge/control-plane gates. In particular:

```bash
python scripts/validate_all.py
python -m pytest -q
```

should be run with a timeout at or above the repo-recorded ceiling when invoked through tools. A timeout is not a validation verdict.

T411's focused setup gates are:

```bash
python scripts/validate_parallel_execution_safety.py --task-id T411 --allow-current-task-dirty --require-task-branch
python scripts/validate_t411_cursor_batch_artifacts.py
python -m pytest tests/test_t411_cursor_batch_artifacts.py -q
python -m pytest tests/test_parallel_execution_safety.py -q
python scripts/validate_task_scope.py --task-id T411
python scripts/agent/validate_handoffs.py
```
