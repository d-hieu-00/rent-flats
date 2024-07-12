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

class GetBillsHandler(BaseRequestHandler):
    def method():   return "GET"
    def path():     return "/api/bills"

    def verify_params(self, in_req_path: str):
        in_params = parse_qs(urlparse(in_req_path).query)
        out_id  = None
        # Try parse params
        try:
            if "id" in in_params:
                out_id = int(in_params["id"][0])
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Out params
        return out_id

    def _handle(self, req: RequestRouter):
        # Parse and verify params
        house_id = self.verify_params(req.path)
        if house_id is None:
            return
        # Check session_id
        session_id = self._read_session_id(req)
        if session_id is None or is_uuid(session_id) == False:
            self._set_resp(403, "Access denied")
            return
        # Get rented house
        db_ret = DBHanlder.dbMain.get_bills(session_id, house_id)
        if is_json(db_ret):
            resp = json.loads(db_ret)
            if resp.keys().__contains__("error"):
                self._set_resp(400, resp["error"])
            else:
                self._set_resp(200, json.dumps(resp))
        else:
            self._set_resp(500, "Failed to get bills")
