import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class CreateHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)

        rewards_db = client["Rewards"]
        rewards = list(rewards_db.rewards.find({}, {"_id": 0}))

        db = client["Users"]
        users = list(db.users.find({}, {"_id": 0}))

        email = self.get_argument("email")
        total = self.get_argument("total")

        db.users.insert({"email": email, "total": total})

        self.write(json.dumps(users) + json.dumps(rewards))
