#!/usr/bin/env python3
"""Start installed Pi with isolated local Ollama settings and calendar-only tools."""
import os
from pathlib import Path
import shutil
import sys
ROOT = Path(__file__).resolve().parent
extra_args = sys.argv[1:]
session_args = ["--no-session"]
if "--record-session" in extra_args:
    index = extra_args.index("--record-session")
    if index + 1 >= len(extra_args):
        raise SystemExit("--record-session requires a directory")
    session_dir = Path(extra_args[index+1]).resolve()
    session_dir.mkdir(parents=True, exist_ok=True)
    session_args = ["--session-dir", str(session_dir)]
    extra_args = extra_args[:index] + extra_args[index+2:]
config = ROOT / ".calendar-pi"
config.mkdir(exist_ok=True)
for source, target in [("provider.example.json", "models.json"), ("settings.example.json", "settings.json")]:
    destination = config / target
    if not destination.exists():
        shutil.copyfile(ROOT / "local-model" / source, destination)
pi = shutil.which("pi")
if not pi:
    raise SystemExit("Pi is not installed. See README.md.")
environment = {**os.environ, "PI_CODING_AGENT_DIR": str(config), "PI_OFFLINE": "1", "PI_TELEMETRY": "0"}
os.chdir(ROOT)
args = [pi, "--offline", *session_args, "--no-extensions", "--extension", str(ROOT / "extensions/calendar.ts"), "--no-mcp", "--no-skills", "--no-prompt-templates", "--no-context-files", "--no-themes", "--no-builtin-tools", "--no-approve", "--tools", "calendar_list,calendar_get,calendar_create,calendar_update,calendar_delete", "--system-prompt", str(ROOT / "local-model/prompt.txt"), "--provider", "ollama-calendar", "--model", "calendar-qwen3.5:4b", "--thinking", "off", *extra_args]
os.execve(pi, args, environment)
