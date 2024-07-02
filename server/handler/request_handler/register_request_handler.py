from handler.request_router import RequestRouter

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from setting.get_config_handler import GetConfigHandler
from setting.set_config_handler import SetConfigHandler

from user.get_user_handler import GetUserHandler
from user.signup_handler import SignupHandler
from user.login_handler import LoginHandler

def register_handler():
    RequestRouter.register_handler(GetConfigHandler.method(), GetConfigHandler.path(), GetConfigHandler)
    RequestRouter.register_handler(SetConfigHandler.method(), SetConfigHandler.path(), SetConfigHandler)

    RequestRouter.register_handler(GetUserHandler.method(), GetUserHandler.path(), GetUserHandler)
    RequestRouter.register_handler(SignupHandler.method(), SignupHandler.path(), SignupHandler)
    RequestRouter.register_handler(LoginHandler.method(), LoginHandler.path(), LoginHandler)

