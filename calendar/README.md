# Calendar Lab
A tiny local calendar with a small CRUD API. Python 3.10+ standard library, SQLite, plain HTML/CSS/JavaScript. No package installation required. All data is fictional; no Google Calendar connection.

## Start
From the repository root, enter the app directory:
```sh
cd calendar
python3 server.py
```
Open http://127.0.0.1:8765 . The server binds only to loopback. An empty calendar is intentional. Add/edit/delete events, navigate months, select a day, or Refresh to see API changes. Stop with Ctrl-C. Events persist in ignored `data/calendar.sqlite3` across restarts. Use `--db /tmp/calendar-demo.sqlite3 --port 8766` for a separate UI sandbox (set CALENDAR_PORT=8766 for Pi).

## Time behavior
UI fields and display are always **UTC**, independent of your Mac/browser timezone. API requires explicit ISO 8601 offsets and normalizes to UTC seconds. End must be after start. Events spanning days appear on every overlapping day; end is exclusive. Overlaps are allowed. There are no recurring/all-day events or notifications.

## HTTP tools
| Operation | Method / path | Body |
| --- | --- | --- |
| List | GET /api/events | — |
| Get | GET /api/events/{id} | — |
| Create | POST /api/events | event |
| Update | PUT /api/events/{id} | full replacement event |
| Delete | DELETE /api/events/{id} | — |

Event: `{"title":"Fictional orbit","start":"2030-04-08T09:00:00Z","end":"2030-04-08T10:00:00Z","location":"Fictional room","notes":"Synthetic test"}`. Create returns a UUID; update preserves it. Required: title/start/end. Omitted location/notes become empty. Errors return JSON `error` with 400, 404, 405 or 415; rejected origins/hosts return 403. List is ordered by start and ID. No auth, no CORS: intended only for local experiments, not deployment.

## Checks
```sh
python3 -m unittest discover -s tests -v
node --check web/app.js
```
Tests use isolated temporary SQLite databases and ephemeral loopback ports, covering CRUD, persistence, time validation and local request restrictions. No cloud services or credentials are configured. Runtime data and logs are ignored by Git.

## Pi with local Ollama
Pi is the agent harness: it sends your request and tool descriptions to a model, runs requested tools and returns their results to the model. Ollama runs the model locally. The calendar API stores events in SQLite. Pi is not itself the model.

Installed here: official Pi 1.3.0, Ollama 0.32.1, Qwen3.5:4b Q4_K_M (3.32 GB download). Ollama already meets the model's >=0.30 requirement, so no update was needed. Existing models and global configuration were preserved. Local inference has no API fees but uses your computer's power and memory; small models can make mistakes.

On another Mac, install Node >=22.19 and Ollama, then:
```sh
npm install -g @earendil-works/pi-coding-agent@1.3.0
ollama pull qwen3.5:4b
ollama create calendar-qwen3.5:4b -f local-model/Modelfile
```
Those steps are already complete here. With Ollama running on http://127.0.0.1:11434 and `python3 server.py` in one terminal, launch Pi in another:
```sh
python3 pi-calendar.py
```
Try “List my calendar events” or “Create a fictional event called Orbit test on April 8, 2030, 09:00–10:00 UTC.” Use exact IDs when modifying/deleting. Escape interrupts a response; Ctrl-C exits. Each launch starts fresh and does not save a session. Refresh the web UI after tool changes.

The five tools are calendar_list, calendar_get, calendar_create, calendar_update and calendar_delete. Update replaces all fields, so fetch the current event first. The launcher disables built-in shell/file tools, MCP, automatic extensions/context/skills, startup networking and telemetry. Its tool allowlist is not an OS sandbox; confirmation is a prompt policy, not a host approval gate. Do not use `/share` for private sessions.

Settings are isolated in ignored `.calendar-pi/`, copied once from local-model examples; global Pi settings remain untouched. The API key is only a dummy local placeholder. Ollama and Pi both use 8192-token context; output is capped at 1024 tokens with reduced compaction reserves. Thinking off maps to `reasoning_effort: none`. No cloud model is configured.

## Verification on this Mac
- Six isolated HTTP/SQLite tests passed; JavaScript and extension syntax checks passed.
- Chrome checks verified create, edit, reload persistence and month navigation. Browser automation disconnected at the delete confirmation, so UI deletion was not fully verified; API deletion passed.
- One synthetic Pi + local Ollama integration smoke test completed in 43.39 seconds against a temporary database: create/get/update/list/delete/list, final database empty. The model omitted end once; validation rejected it and the model corrected the call. No model errors or thinking blocks; agent_settled reported not aborted.
- This was an integration smoke test, not student failure-study evidence or reflection. Raw traces remain ignored under output/.

## Folder layout
Everything specific to this app lives under `calendar/`:
- `server.py`, `web/`: loopback HTTP server, CRUD API and browser UI.
- `data/calendar.sqlite3`: persistent SQLite database (ignored).
- `extensions/`, `pi-calendar.py`, `local-model/`: Pi tools, launcher and local-model configuration templates.
- `.calendar-pi/`: project-local Pi configuration (ignored, preserved across launches).
- `tests/`: isolated CRUD/persistence checks; run the documented test command from `calendar/`.
- `output/`: local diagnostic logs and traces (ignored).

Server and launcher paths resolve relative to their files, so `python3 calendar/server.py` and `python3 calendar/pi-calendar.py` also work from the repository root. The default database remains inside this folder regardless of your working directory. An explicitly supplied relative `--db` path is relative to your working directory.

Pi and Ollama executables, the Python/Node runtimes, and downloaded Ollama model weights remain installed outside the repository. Moving this folder does not bundle those external dependencies or reinstall them.
