import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson.json_util import loads
from bson.json_util import dumps

class CreateHandler(tornado.web.RequestHandler):
    # http://localhost:7050/create?emailAddress=bob@gmail.com&orderTotal=220
    @coroutine
    def get(self):
        emailAddress = self.get_argument("emailAddress")
        orderTotal = self.get_argument("orderTotal")
        rewardsPoints = int(float(orderTotal))

        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        rewards = list(rewards_db.rewards.find({}, {"_id": 0}))

        rewardLevel = None
        nextRewardLevel = None
        for reward in rewards:
            if rewardsPoints >= reward.get("points"):
                rewardLevel = reward
            elif rewardsPoints < reward.get("points"):
                nextRewardLevel = reward
                break
            
        rewardsProgress = (nextRewardLevel.get("points") - rewardsPoints) / 100

        user_data = {
            "emailAddress": emailAddress, 
            "rewardsPoints": rewardsPoints,
            "rewardsTier": rewardLevel.get("tier"),
            "rewardsTierName": rewardLevel.get("rewardName"),
            "nextRewardsTier": nextRewardLevel.get("tier"),
            "nextRewardsTierName": nextRewardLevel.get("rewardName"),
            "nextRewadsTierProgress": rewardsProgress
        }

        db = client["Users"]
        # db.users.remove()
        db.users.insert(user_data)

        self.write(dumps(user_data))
