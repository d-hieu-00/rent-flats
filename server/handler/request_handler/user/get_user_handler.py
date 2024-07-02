import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetUserHandler(BaseRequestHandler):
    def method():   return "GET"
    def path():     return "/api/user"

    def _handle(self, _: RequestRouter):
        host = self._read_header(_, 'host')
        print(host)
        response = DBHanlder.dbMain.get_user_by_session_id('097054c7-ea47-413f-a518-fc7478efae8d')
        if response is None:
            self._set_resp(500, "Failed to query user")
        else:
            self._set_resp(200, response)
