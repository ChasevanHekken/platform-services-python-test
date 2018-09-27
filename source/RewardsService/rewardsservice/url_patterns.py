from handlers.rewards_handler import RewardsHandler
from handlers.main_handler import MainHandler
from handlers.create_handler import CreateHandler

url_patterns = [
    (r'/', MainHandler),
    (r'/create', CreateHandler),
    (r'/rewards', RewardsHandler),
]
