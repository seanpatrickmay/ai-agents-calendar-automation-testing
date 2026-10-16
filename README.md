# AI Agents Calendar Automation Testing

The local SQLite calendar, CRUD API, web UI, Pi tools, tests and app documentation live in [`calendar/`](calendar/README.md).

From this repository root:
```sh
python3 calendar/server.py
```
Open http://127.0.0.1:8765 . In another terminal:
```sh
python3 calendar/pi-calendar.py
```
See the [calendar README](calendar/README.md) for setup, API details and tests. Pi, Ollama and downloaded model weights are external installations; application data and local Pi configuration stay inside `calendar/` and are ignored by Git.

## Inputs and evidence
- [`test-context/`](test-context/): fictional bot-readable task input; currently only the exact existing integration smoke-test request. Nothing loads automatically.
- [`evidence/`](evidence/README.md): actual-run inventory and evaluator notes. Original smoke-test traces live in ignored `evidence/local/`, not on GitHub.
- `calendar/tests/`: application unit/integration tests, kept with the app.

There is no assignment experiment dataset or student study evidence yet. See the evidence inventory for the distinction from the earlier standalone scaffold.
