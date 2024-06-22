from handler.request_router import RequestRouter

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from setting.get_config_handler import GetConfigHandler
from setting.set_config_handler import SetConfigHandler

def register_handler():
    RequestRouter.register_handler(GetConfigHandler.method(), GetConfigHandler.path(), GetConfigHandler)
    RequestRouter.register_handler(SetConfigHandler.method(), SetConfigHandler.path(), SetConfigHandler)

