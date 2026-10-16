"""Seed only a new isolated fictional scenario database; never reset existing data."""
import json
from pathlib import Path
import sys
APP = Path(__file__).resolve().parents[2]
REPO = APP.parent
sys.path.insert(0,str(APP))
from server import Store, validate
path = APP / "data/interview-reschedule.sqlite3"
if path.exists():
    raise SystemExit(f"Preserving existing scenario database: {path}")
events = json.loads((REPO / "test-context/interview-reschedule/events.json").read_text())
validated = [{"id": event["id"], **validate({k:v for k,v in event.items() if k != "id"})} for event in events]
store = Store(path)
with store.connect() as db:
    db.executemany("INSERT INTO events VALUES (:id,:title,:start,:end,:location,:notes)",validated)
print(f"Created {len(validated)} fictional events in {path}")
