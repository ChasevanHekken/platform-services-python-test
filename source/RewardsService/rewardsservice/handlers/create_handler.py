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

        emailAddress = self.get_argument("emailAddress")
        orderTotal = self.get_argument("orderTotal")

        user_data = {
            "emailAddress": emailAddress, 
            "rewardsPoints": int(float(orderTotal))
        }

        db.users.insert(user_data)
        chase = db.users.find({"emailAddress": "joe"})
        self.write(dumps(chase))
