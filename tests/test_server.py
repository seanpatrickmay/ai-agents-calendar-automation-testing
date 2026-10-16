"""Isolated deterministic CRUD checks, not model experiments."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from server import make_server, Store

class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/"test.sqlite3"
        self.server=make_server(self.path,0)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.stop)
        self.base=f"http://127.0.0.1:{self.server.server_port}"
        self.event={"title":"Fictional orbit","start":"2030-04-08T09:00:00+02:00","end":"2030-04-08T10:00:00+02:00","location":"Fictional room"}
    def stop(self):self.server.shutdown();self.server.server_close();self.thread.join()
    def request(self,method,path="/api/events",body=None,headers=None):
        h={"Content-Type":"application/json",**(headers or {})}
        req=Request(self.base+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers=h)
        try:
            with urlopen(req) as response:return response.status,json.loads(response.read())
        except HTTPError as error:return error.code,json.loads(error.read())
    def test_crud_and_persistence(self):
        status,event=self.request("POST",body=self.event);self.assertEqual(status,201)
        self.assertEqual(event["start"],"2030-04-08T07:00:00Z")
        path="/api/events/"+event["id"]
        self.assertEqual(self.request("GET",path),(200,event))
        self.assertEqual(self.request("GET")[1],[event])
        self.assertEqual(Store(self.path).get(event["id"]),event)
        updated={**self.event,"title":"Fictional revised"}
        status,new=self.request("PUT",path,updated);self.assertEqual(status,200);self.assertEqual(new["id"],event["id"])
        self.assertEqual(Store(self.path).get(event["id"])["title"],updated["title"])
        self.assertEqual(self.request("DELETE",path)[0],200)
        self.assertEqual(self.request("GET",path)[0],404)
        self.assertEqual(Store(self.path).list(),[])
    def test_invalid_times_and_fields(self):
        for change in [{"start":"2030-04-08T09:00:00"},{"end":self.event["start"]},{"end":"bad"},{"title":" "},{"id":"override"}]:
            self.assertEqual(self.request("POST",body={**self.event,**change})[0],400)
        self.assertEqual(self.request("GET")[1],[])
    def test_missing_ids(self):
        for method in ["GET","PUT","DELETE"]:
            self.assertEqual(self.request(method,"/api/events/missing",self.event if method=="PUT" else None)[0],404)
    def test_cross_origin_and_host(self):
        self.assertEqual(self.request("POST",body=self.event,headers={"Origin":"https://example.com"})[0],403)
        self.assertEqual(self.request("GET",headers={"Host":"example.com"})[0],403)
    def test_static_ui(self):
        for path in ["/","/app.js","/style.css"]:
            with urlopen(self.base+path) as response:self.assertEqual(response.status,200);self.assertTrue(response.read())
    def test_wrong_content_type(self):
        self.assertEqual(self.request("POST",body=self.event,headers={"Content-Type":"text/plain"})[0],415)
