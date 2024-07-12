import sys, pathlib
import json
from urllib.parse import parse_qs, urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import is_json
from utils.utils import is_uuid
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetHousesHandler(BaseRequestHandler):
    def method():   return "GET"
    def path():     return "/api/houses"

    def verify_params(self, in_req_path: str):
        in_params = parse_qs(urlparse(in_req_path).query)
        out_address  = None
        # Try parse params
        try:
            if "address" in in_params:
                out_address = in_params["address"][0]
            else:
                out_address = ""
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Out params
        return out_address

    def _handle(self, req: RequestRouter):
        # Parse and verify params
        in_address = self.verify_params(req.path)
        if in_address is None:
            return
        # Get houses
        db_ret = DBHanlder.dbMain.get_houses(in_address)
        if is_json(db_ret):
            resp = json.loads(db_ret)
            if resp.keys().__contains__("error"):
                self._set_resp(400, resp["error"])
            else:
                self._set_resp(200, json.dumps(resp))
        else:
            self._set_resp(500, "Failed to get rented houses")