import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CreateHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        email = self.get_argument("email")
        total = self.get_argument("total")
        self.write(email + total)
