import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson.json_util import loads
from bson.json_util import dumps

class FindHandler(tornado.web.RequestHandler):
    # http://localhost:7050/find?emailAddress=joe@gmail.com
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Users"]
        user = db.users.find({"emailAddress": self.get_argument("emailAddress")})
        self.write(dumps(user))