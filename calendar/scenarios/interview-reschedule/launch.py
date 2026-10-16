"""Open Pi with fictional context and session recording; do not submit a task."""
from pathlib import Path
import os
import sys
APP = Path(__file__).resolve().parents[2]
REPO = APP.parent
os.environ["CALENDAR_PORT"] = "8766"
os.execv(sys.executable, [sys.executable, str(APP / "pi-calendar.py"), "--record-session", str(REPO / "evidence/local/interview-reschedule/sessions"), "--append-system-prompt", str(REPO / "test-context/interview-reschedule/context.md")])
