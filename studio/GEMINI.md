# Gemini entry point

Everything in this folder is governed by `AGENTS.md`; `PROMPT.md` gives the principles. Read both first and follow them exactly.

@./PROMPT.md
@./AGENTS.md

Gemini-specific notes:
- Calendar access: run `python3 ../calendar/server.py`, then use the REST API at `http://127.0.0.1:8765/api/events` (see `config/TOOLS.md` for the five operations and the event fields).
- Stable IDs: compute `sha1(course + item_type + due_date + title)[:10]` in a shell (e.g. `python3 -c`), concatenated with no separators.
- Shell and file writes are allowed only where `AGENTS.md` §2 says. `config/` and `user_files/` are read-only.
