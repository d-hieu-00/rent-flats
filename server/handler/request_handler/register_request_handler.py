from handler.request_router import RequestRouter

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from setting.get_config_handler import GetConfigHandler
from setting.set_config_handler import SetConfigHandler

from user.get_user_handler import GetUserHandler
from user.signup_handler import SignupHandler
from user.login_handler import LoginHandler
from user.logout_handler import LogoutHandler

from house.get_houses_handler import GetHousesHandler
from house.get_rented_houses_handler import GetRentedHousesHandler
from house.get_bills_handler import GetBillsHandler

def register_handler():
    RequestRouter.register_handler(GetConfigHandler.method(), GetConfigHandler.path(), GetConfigHandler)
    RequestRouter.register_handler(SetConfigHandler.method(), SetConfigHandler.path(), SetConfigHandler)

    RequestRouter.register_handler(GetUserHandler.method(), GetUserHandler.path(), GetUserHandler)
    RequestRouter.register_handler(SignupHandler.method(), SignupHandler.path(), SignupHandler)
    RequestRouter.register_handler(LoginHandler.method(), LoginHandler.path(), LoginHandler)
    RequestRouter.register_handler(LogoutHandler.method(), LogoutHandler.path(), LogoutHandler)

    RequestRouter.register_handler(GetHousesHandler.method(), GetHousesHandler.path(), GetHousesHandler)
    RequestRouter.register_handler(GetRentedHousesHandler.method(), GetRentedHousesHandler.path(), GetRentedHousesHandler)
    RequestRouter.register_handler(GetBillsHandler.method(), GetBillsHandler.path(), GetBillsHandler)

