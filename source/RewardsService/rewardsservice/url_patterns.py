from handlers.rewards_handler import RewardsHandler
from handlers.main_handler import MainHandler
from handlers.create_handler import CreateHandler
from handlers.find_handler import FindHandler
from handlers.users_handler import UsersHandler

url_patterns = [
    (r'/', MainHandler),
    (r'/create', CreateHandler),
    (r'/find', FindHandler),
    (r'/users', UsersHandler),
    (r'/rewards', RewardsHandler),
]
