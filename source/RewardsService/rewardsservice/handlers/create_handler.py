import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson.json_util import loads
from bson.json_util import dumps

class CreateHandler(tornado.web.RequestHandler):
    # http://localhost:7050/create
    # {
    #     "emailAddress": "chase@gmail.com", 
    #     "orderTotal": "500",
    # }
    # POST request

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        rewards = list(rewards_db.rewards.find({}, {"_id": 0}))
        db = client["Users"]
        # db.users.remove()

        emailAddress = self.get_argument("emailAddress")
        orderTotal = self.get_argument("orderTotal")
        rewardsPoints = int(float(orderTotal))

        user = db.users.find_one({"emailAddress": emailAddress})
        if user:
            rewardsPoints = rewardsPoints + user.get("rewardsPoints")
        if rewardsPoints > 1000:
            rewardsPoints = 1000

        rewardLevel = None
        nextRewardLevel = None
        for reward in rewards:
            if rewardsPoints >= reward.get("points"):
                rewardLevel = reward
            elif rewardsPoints <= reward.get("points"):
                nextRewardLevel = reward
                break
            
        if rewardsPoints < 100:
            user_data = {
                "emailAddress": emailAddress, 
                "rewardsPoints": rewardsPoints,
                "rewardsTier": "N/A",
                "rewardsTierName": "N/A",
                "nextRewardsTier": "A",
                "nextRewardsTierName": "5% off purchase",
                "nextRewadsTierProgress": (100 - rewardsPoints) / 100
            }
        elif rewardsPoints >= 1000:
            user_data = {
                "emailAddress": emailAddress, 
                "rewardsPoints": rewardsPoints,
                "rewardsTier": rewardLevel.get("tier"),
                "rewardsTierName": rewardLevel.get("rewardName"),
                "nextRewardsTier": "N/A",
                "nextRewardsTierName": "N/A",
                "nextRewadsTierProgress": "N/A"
            }
        else:
            user_data = {
                "emailAddress": emailAddress, 
                "rewardsPoints": rewardsPoints,
                "rewardsTier": rewardLevel.get("tier"),
                "rewardsTierName": rewardLevel.get("rewardName"),
                "nextRewardsTier": nextRewardLevel.get("tier"),
                "nextRewardsTierName": nextRewardLevel.get("rewardName"),
                "nextRewadsTierProgress": (nextRewardLevel.get("points") - rewardsPoints) / 100
            }

        if user:
            user = db.users.update({"emailAddress": emailAddress}, user_data)
        else:
            db.users.insert(user_data)

        self.write(dumps(user_data))
        # self.write(dumps(user))

