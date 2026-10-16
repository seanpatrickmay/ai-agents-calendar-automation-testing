#!/usr/bin/env python3
"""Start Pi in studio/ with the local Ollama model, studio files and the calendar tools.

Reuses ../calendar/extensions/calendar.ts and ../calendar/local-model/* so model
and calendar settings live in one place. Start ../calendar/server.py first.
Stable IDs come from the stable_id tool (extensions/stable_id.ts), so shell is off.
Set STUDIO_BASH=1 only if you want shell as well.
Sessions are saved as JSONL under ../evidence/local/studio-sessions/ (Git-ignored).
"""
import os
from pathlib import Path
import shutil
import sys
ROOT = Path(__file__).resolve().parent
CALENDAR = ROOT.parent / "calendar"
config = ROOT / ".studio-pi"
config.mkdir(exist_ok=True)
for source, target in [("provider.example.json", "models.json"), ("settings.example.json", "settings.json")]:
    destination = config / target
    if not destination.exists():
        shutil.copyfile(CALENDAR / "local-model" / source, destination)
pi = shutil.which("pi")
if not pi:
    raise SystemExit("Pi is not installed. See ../calendar/README.md.")
tools = ["read", "write", "edit", "grep", "find", "ls", "stable_id"] + (["bash"] if os.environ.get("STUDIO_BASH") == "1" else [])
tools += ["calendar_list", "calendar_get", "calendar_create", "calendar_update", "calendar_delete"]
environment = {**os.environ, "PI_CODING_AGENT_DIR": str(config), "PI_OFFLINE": "1", "PI_TELEMETRY": "0"}
sessions = ROOT.parent / "evidence/local/studio-sessions"
sessions.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
args = [pi, "--offline", "--session-dir", str(sessions), "--no-extensions", "--extension", str(CALENDAR / "extensions/calendar.ts"), "--extension", str(ROOT / "extensions/stable_id.ts"), "--no-mcp", "--no-skills", "--no-prompt-templates", "--no-themes", "--no-approve", "--tools", ",".join(tools), "--system-prompt", str(ROOT / "PROMPT.md"), "--provider", "ollama-calendar", "--model", "calendar-qwen3.5:27b", "--thinking", "off", *sys.argv[1:]]
os.execve(pi, args, environment)
