import sys, pathlib
import re
import json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import is_json
from utils.utils import hash_password
from copy import deepcopy

from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class SignupHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/signup"

    def _validate_data(self, key, data):
        data = data.strip()
        if type(data) != type(""):
            return "Invalid data"
        if key == "username" and (len(data) > 256 or re.match(r"^[a-zA-Z0-9 _-]{4,256}$", data) == None or len(data) < 4):
            return "Username must be larger than 4 and less than 256 characters. Allow characters a-z0-9,'_','-' and whitespace."
        if key == "password" and (len(data) > 256 or len(data) < 4):
            return "Password must be larger than 4 and less than 256 characters."
        if key == "email" and (re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data) == None):
            return "Invalid email"
        return None

    def _validate_body(self, data):
        for k in ["username", "password", "email"]:
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
        # Strip whitespace
        body["username"] = body["username"].strip()
        body["password"] = body["password"].strip()
        body["email"] = body["email"].strip()
        # Validate data
        err = self._validate_body(body)
        if err is not None:
            self._set_resp(400, err)
            return
        # Generate pass
        salt_pass, hashed_pass = hash_password(body["password"])

        db_body = deepcopy(body)
        db_body["salt"] = salt_pass.decode()
        db_body["password"] = hashed_pass.decode()
        db_body["additional"] = json.dumps({})

        response = DBHanlder.dbMain.new_user(json.dumps(db_body))
        if is_json(response):
            resp = json.loads(response)
            if resp.keys().__contains__("error"):
                self._set_resp(400, resp["error"])
            else:
                del resp["password"]
                del resp["salt"]
                del resp["admin"]
                self._set_resp(200, json.dumps(resp))
        else:
            self._set_resp(500, "Failed to create user")
