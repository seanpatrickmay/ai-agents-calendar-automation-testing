# Evidence inventory

This directory contains evidence and evaluator-facing notes, not bot context. Do not pass it to the model as task input.

## Actual existing run: integration smoke test
One local Pi 1.3.0 + Ollama 0.32.1 + Qwen3.5 4B integration run was performed on 2026-10-16 against a temporary SQLite database. It completed in 43.39 seconds. Tool records show create, get, update, list, delete and final list. The first update omitted end and was rejected; a corrected update succeeded. The final database was empty, no model errors or thinking blocks were recorded, and agent_settled reported aborted=false.

This is integration verification, NOT an assignment study observation, repeated failure episode, student interpretation or reflection. No new model run was performed during this reorganization.

The original files were moved byte-for-byte from calendar/output/ to:
- `local/integration-smoke/pi-smoke.jsonl`: actual complete JSONL trace.
- `local/integration-smoke/pi-smoke-summary.json`: summary extracted from the actual run.
- `local/integration-smoke/pi-smoke.stderr.log`: empty stderr capture.

These raw files remain local and ignored by Git, so they will NOT appear in a fresh clone or on GitHub. They may contain machine/session metadata. Review and redact a copy before deliberately publishing evidence. Do not force-add private logs. File checksums below document the moved originals.

## Other checks
Six isolated HTTP/SQLite tests passed before and after the calendar/ move. Their fictional event objects remain inside calendar/tests/test_server.py; they are code-test fixtures, not bot input.
Browser checks verified create, edit, reload persistence and navigation. Deletion UI verification was interrupted by browser automation disconnection. API deletion passed. No saved screenshot artifact exists.
Calendar server diagnostic logs stay in ignored calendar/output/. Transient test databases were temporary; the app's live database stays in ignored calendar/data/ and was not changed by this reorganization.

## Bot inputs and earlier scaffold
`../test-context/integration-smoke-task.txt` is the exact fictional user task already used in the integration run, recovered from its runner. It contains no evaluator commentary. The launcher does not automatically load test-context/ or evidence/; supply only a chosen task explicitly. Runtime system instructions remain in calendar/local-model/prompt.txt because they are application configuration.

The separate local sibling calendar-control-lab/ (outside this Git repository) contains a three-event fictional calendar fixture, E1/E2/E3 candidate prompts with expected behavior, baseline/approval experiment plans, a run protocol, blank results template and deterministic test evidence. Its combined cases.json includes evaluator expectations, so it must not be supplied wholesale as bot context. It has no actual model study runs. None of that scaffold was copied here.

No assignment dataset, three observed failure episodes attempted twice, student reflection answers or fabricated evidence has been created in this repository.

## Original file SHA-256
- `pi-smoke.jsonl`: `4f79cb3b3201555c079f77fc49fbd9c2aa408abca1ae482304a1250454e3ca3f`
- `pi-smoke-summary.json`: `16408bcbb5f06b2ebfb0a49ebb0704cf313661604278c68e70b6c54ca14110a2`
- `pi-smoke.stderr.log`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
