import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class MainHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.write('<h1>hello world</a>')
