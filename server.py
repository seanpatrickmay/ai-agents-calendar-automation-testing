#!/usr/bin/env python3
"""Local synthetic calendar. Python standard library only."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sqlite3
from urllib.parse import urlsplit
from uuid import uuid4

ROOT = Path(__file__).resolve().parent

def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Times must be ISO 8601 strings with an explicit offset")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid ISO 8601 time")
    if parsed.utcoffset() is None:
        raise ValueError("An explicit timezone offset is required")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def validate(data):
    if not isinstance(data, dict) or set(data) - {"title", "start", "end", "location", "notes"}:
        raise ValueError("Use title, start, end, location and notes only")
    result = {k: data.get(k, "") for k in ("title", "start", "end", "location", "notes")}
    if not all(isinstance(v, str) for v in result.values()):
        raise ValueError("All fields must be strings")
    result["title"] = result["title"].strip()
    if not result["title"] or any(len(v) > 10000 for v in result.values()):
        raise ValueError("Title is required; fields must be at most 10000 characters")
    result["start"], result["end"] = timestamp(result["start"]), timestamp(result["end"])
    if result["end"] <= result["start"]:
        raise ValueError("End must be after start")
    return result

class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, title TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL, location TEXT NOT NULL, notes TEXT NOT NULL)")
    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db
    def list(self):
        with self.connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM events ORDER BY start, id")]
    def get(self, event_id):
        with self.connect() as db:
            row = db.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
            if row is None: raise KeyError("Event not found")
            return dict(row)
    def create(self, data):
        event = {"id": str(uuid4()), **validate(data)}
        with self.connect() as db:
            db.execute("INSERT INTO events VALUES (:id,:title,:start,:end,:location,:notes)", event)
        return event
    def update(self, event_id, data):
        event = {"id": event_id, **validate(data)}
        with self.connect() as db:
            result = db.execute("UPDATE events SET title=:title,start=:start,end=:end,location=:location,notes=:notes WHERE id=:id", event)
            if result.rowcount != 1: raise KeyError("Event not found")
        return event
    def delete(self, event_id):
        with self.connect() as db:
            if db.execute("DELETE FROM events WHERE id=?", (event_id,)).rowcount != 1:
                raise KeyError("Event not found")

def make_server(path, port=8765):
    store = Store(path)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def reply(self, status, body, content_type="application/json"):
            raw = json.dumps(body).encode() if content_type == "application/json" else body
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'")
            self.end_headers(); self.wfile.write(raw)
        def handle_request(self):
            authority = f"127.0.0.1:{self.server.server_port}"
            allowed = {authority, f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in allowed:
                return self.reply(403, {"error":"Local Host required"})
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://" + host for host in allowed}:
                return self.reply(403, {"error":"Cross-origin requests are disabled"})
            path = urlsplit(self.path).path
            if self.command == "GET" and path in {"/", "/app.js", "/style.css"}:
                name, mime = {"/":("index.html","text/html; charset=utf-8"),"/app.js":("app.js","text/javascript; charset=utf-8"),"/style.css":("style.css","text/css; charset=utf-8")}[path]
                return self.reply(200, (ROOT / "web" / name).read_bytes(), mime)
            if path != "/api/events" and not path.startswith("/api/events/"):
                return self.reply(404, {"error":"Not found"})
            event_id = path[len("/api/events/"):] if path.startswith("/api/events/") else None
            try:
                data = None
                if self.command in {"POST","PUT"}:
                    if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                        return self.reply(415, {"error":"Use application/json"})
                    size = int(self.headers.get("Content-Length", "0"))
                    if size < 1 or size > 65536: raise ValueError("Body must be 1–65536 bytes")
                    data = json.loads(self.rfile.read(size))
                if self.command == "GET": return self.reply(200, store.get(event_id) if event_id is not None else store.list())
                if self.command == "POST" and event_id is None: return self.reply(201, store.create(data))
                if self.command == "PUT" and event_id: return self.reply(200, store.update(event_id, data))
                if self.command == "DELETE" and event_id:
                    store.delete(event_id); return self.reply(200, {"deleted":event_id})
                return self.reply(405, {"error":"Method not allowed"})
            except KeyError: return self.reply(404, {"error":"Event not found"})
            except (ValueError, UnicodeDecodeError) as error: return self.reply(400, {"error":str(error)})
        do_GET = do_POST = do_PUT = do_DELETE = handle_request
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--db", type=Path, default=ROOT / "data/calendar.sqlite3")
    args = parser.parse_args()
    server = make_server(args.db, args.port)
    print(f"Synthetic calendar: http://127.0.0.1:{server.server_port}", flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
