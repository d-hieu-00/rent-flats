import sys, pathlib
import json

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

    def _handle(self, req: RequestRouter):
        # Check session_id
        session_id = self._read_session_id(req)
        # if session_id is None or is_uuid(session_id) == False:
        #     self._set_resp(403, "Access denied")
        #     return
        # Dummy data
        # TODO: udpate with actual data
        self._set_resp(200, json.dumps({"houses": [
            {
                "house_id": 1,
                "address": "123 Mai Chí Thọ St, Thủ Đức",
                "capacity": 5,
                "base_price": 10000000,
                "additional": {
                    "type": "apartment",
                    "description": "Happy Residence Charming apartment for rent",
                    "images": [
                        "/__images/houses/1/1.jpg",
                        "/__images/houses/1/2.jpg",
                        "/__images/houses/1/3.jpg",
                    ],
                }
            },
            {
                "house_id": 2,
                "address": "456 Lý Thái Tổ St, Thủ Đức",
                "capacity": 3,
                "base_price": 8000000,
                "additional": {
                    "type": "house",
                    "description": "Lovely Villa with beautiful views",
                    "images": [
                        "/__images/houses/2/1.jpg",
                        "/__images/houses/2/2.jpg",
                        "/__images/houses/2/3.jpg",
                    ],
                }
            }
        ]}))

