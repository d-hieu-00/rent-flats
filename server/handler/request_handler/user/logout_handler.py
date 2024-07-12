import sys, pathlib
import json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import is_json
from utils.utils import is_uuid
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class LogoutHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/logout"

    def _handle(self, req: RequestRouter):
        # Check session_id
        session_id = self._read_session_id(req)
        if session_id is None or is_uuid(session_id) == False:
            self._set_resp(403, "Access denied")
            return
        # Find user
        db_ret = DBHanlder.dbMain.end_session(session_id)
        if db_ret is None:
            self._set_resp(500, "Failed to logout")
        if is_json(db_ret):
            resp = json.loads(db_ret)
            if resp.keys().__contains__("error"):
                self._set_resp(400, resp["error"])
            else:
                self._set_header("Set-Cookie", "session_id=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
                self._set_resp(200, db_ret)
        else:
            self._set_resp(500, "Failed to login")
