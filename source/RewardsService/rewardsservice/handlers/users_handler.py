import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UsersHandler(tornado.web.RequestHandler):
    # http://localhost:7050/users
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Users"]
        users = list(db.users.find({}, {"_id": 0}))
        self.write(json.dumps(users))