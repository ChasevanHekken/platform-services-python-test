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

        emailAddress = self.get_argument("emailAddress")
        orderTotal = self.get_argument("orderTotal")
        rewardsPoints = int(float(orderTotal))
        
        rewardLevel = None

        for reward in rewards:
            if rewardsPoints >= reward.get("points"):
                rewardLevel = reward
            elif rewardsPoints < reward.get("points"):
                break
            
        user_data = {
            "emailAddress": emailAddress, 
            "rewardsPoints": rewardsPoints,
            "rewardsTier": rewardLevel.get("tier"),
            "rewardsTierName": "name",
            "nextRewardsTier": "next",
            "nextRewardsTierName": "next name",
            "nextRewadsTierProgress": "progress"
        }

        db.users.insert(user_data)
        users = list(db.users.find({}, {"_id": 0}))
        chase = db.users.find({"emailAddress": "joe"})
        self.write(json.dumps(users))
