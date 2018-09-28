import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson.json_util import loads
from bson.json_util import dumps

class CreateHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)

        rewards_db = client["Rewards"]
        rewards = list(rewards_db.rewards.find({}, {"_id": 0}))

        db = client["Users"]
        # db.users.remove()
        users = list(db.users.find({}, {"_id": 0}))

        email = self.get_argument("email")
        total = self.get_argument("total")

        user_data = {
            "emailAddress": email, 
            "rewardsPoints": total
        }

        db.users.insert(user_data)
        chase = db.users.find({"email": "chase"})
        self.write(dumps(chase))
