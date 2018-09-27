from handlers.rewards_handler import RewardsHandler
from handlers.main_handler import MainHandler

url_patterns = [
    (r'/', MainHandler),
    (r'/rewards', RewardsHandler),
]
