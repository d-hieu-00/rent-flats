import sys, pathlib
import re, json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import is_json
from utils.utils import verify_password
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class LoginHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/login"

    def _validate_data(self, key, data):
        if type(data) != type(""):
            return "Invalid data"
        if key == "username" and len(data) > 512:
            return "Username or email must be less than 512 characters."
        if key == "password" and (len(data) > 256):
            return "Password must be less than 256 characters."
        return None

    def _validate_body(self, data):
        for k in ["username", "password"]:
            if data.keys().__contains__(k) != True:
                return f"Missing {k}"
            err = self._validate_data(k, data[k])
            if err is not None:
                return err
        return None

    def _handle(self, req: RequestRouter):
        body = self._read_body(req).decode('utf-8')
        # Check config format
        if body is None or is_json(body) == False:
            self._set_resp(400, "Invalid body")
            return
        body = json.loads(body)
        err = self._validate_body(body)
        if err is not None:
            self._set_resp(400, err)
            return
        # Find user
        db_ret = DBHanlder.dbMain.find_user(body["username"], 0)
        if db_ret is None:
            self._set_resp(500, "Failed to login")
        if is_json(db_ret):
            resp = json.loads(db_ret)
            if resp.keys().__contains__("error"):
                self._set_resp(400, resp["error"])
                return
        else:
            self._set_resp(500, "Failed to login")
            return
        # Check pass
        db_ret = json.loads(db_ret)
        session_id = ""
        if verify_password(db_ret["password"], body["password"]):
            session = DBHanlder.dbMain.new_session(db_ret["user_id"], req.address_string())
            if is_json(session):
                sess = json.loads(session)
                if sess.keys().__contains__("error"):
                    self._set_resp(400, sess["error"])
                    return
                if sess.keys().__contains__("session_id") == "False":
                    self._set_resp(400, "Failed to login")
                    return
                session_id = sess["session_id"]
            else:
                self._set_resp(400, "Failed to login")
                return
        else:
            self._set_resp(400, "Invalid user or password")
            return
        self._set_header("Set-Cookie", f"session_id={session_id}; path=/")
        self._set_resp(200, json.dumps({ "session_id": session_id }))
