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

        user_data = {
            "emailAddress": emailAddress, 
            "rewardsPoints": rewardsPoints,
        }

        if rewardsPoints < 100:
            user_data["rewardsTier"] = "N/A"
            user_data["rewardsTierName"] = "N/A",
            user_data["nextRewardsTier"] = "A",
            user_data["nextRewardsTierName"] = "5% off purchase",
            user_data["nextRewadsTierProgress"] = (100 - rewardsPoints) / 100
        elif rewardsPoints >= 1000:
            user_data["rewardsTier"] = rewardLevel.get("tier")
            user_data["rewardsTierName"] = rewardLevel.get("rewardName")
            user_data["nextRewardsTier"] = "N/A"
            user_data["nextRewardsTierName"] = "N/A"
            user_data["nextRewadsTierProgress"] = "N/A"
        else:
            user_data["rewardsTier"] = rewardLevel.get("tier")
            user_data["rewardsTierName"] = rewardLevel.get("rewardName")
            user_data["nextRewardsTier"] = nextRewardLevel.get("tier")
            user_data["nextRewardsTierName"] = nextRewardLevel.get("rewardName")
            user_data["nextRewadsTierProgress"] = (nextRewardLevel.get("points") - rewardsPoints) / 100
            
        if user:
            db.users.update({"emailAddress": emailAddress}, user_data)
        else:
            db.users.insert(user_data)

        self.write(dumps(user_data))
        # self.write(dumps(user))

