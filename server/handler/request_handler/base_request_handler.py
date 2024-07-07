import sys, pathlib
import json
import http.cookies

from abc import ABC, abstractmethod
from handler.request_router import RequestRouter

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from utils.utils import logger
from utils.utils import is_json
from utils.utils import is_uuid

class BaseRequestHandler(ABC):
    @classmethod
    @abstractmethod
    def method():
        pass

    @classmethod
    @abstractmethod
    def path():
        pass

    @property
    def __server_name(self) -> str:
        return "hehe"

    def __init__(self) -> None:
        super().__init__()
        self._resp_headers = {}
        self._resp_code = 400
        self._resp_msg  = "Unhandle"

    @abstractmethod
    def _handle(self, req: RequestRouter):
        pass

    def _read_body(self, req: RequestRouter, max_len: int = 10 * 1024 * 1024):
        # Expect request body has less than 10MB data
        # If it is larger. Define your own function to read and parse from stream
        length = self._read_header(req, "content-length")
        if length is None:
            logger.warn("Request have no body to read")
            return None
        body_len = int(length)
        if body_len > max_len:
            logger.warn(f"Request body is to larger -- max_len: {max_len}, req_size: {body_len}")
            return None
        return req.rfile.read(body_len)

    def _set_header(self, name, value):
        self._resp_headers[name] = value

    def _send_header(self, req):
        req.send_header("Server", self.__server_name)
        for name in  self._resp_headers.keys():
            req.send_header(name, self._resp_headers[name])

    def _set_resp(self, code: int, msg: str):
        self._resp_code = code
        self._resp_msg  = msg
        # Print log for error resp
        if code != 200:
            logger.warn(f"{self.__req_line} -- Handle failed [{self._resp_code}]: {self._resp_msg}")

    def _send_resp(self, req: RequestRouter):
        if self._resp_code == 403 or self._resp_code == 405 and self._read_session_id(req) is not None:
            self._set_header("Set-Cookie", "session_id=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")
        req.send_response(self._resp_code)
        self._send_header(req)
        if self._resp_code == 200 and self._resp_msg is not None:
            req.send_header('Content-type', 'application/json' if is_json(self._resp_msg) else 'text/plain')
            req.end_headers()
            req.wfile.write(self._resp_msg.encode())
        elif self._resp_code != 200:
            req.send_header('Content-type', 'application/json')
            req.end_headers()
            req.wfile.write(json.dumps({
                "error": self._resp_msg if self._resp_msg is not None else "Something went wrong"
            }).encode())
        else:
            req.end_headers()

    def _read_header(self, req, name):
        name = name.lower(); lst = []
        for _name in req.headers.keys():
            if _name.lower() == name:
                lst.append(req.headers[_name])
        return None if len(lst) == 0 else lst[-1]

    def _read_session_id(self, req):
        cookie_str = self._read_header(req, 'cookie')
        if cookie_str is None:
            return None
        cookie_jar = http.cookies.SimpleCookie(cookie_str)
        if "session_id" in cookie_jar:
            session_id = cookie_jar["session_id"].value
            return session_id if is_uuid(session_id) else None
        else:
            return None

    def handle(self, req: RequestRouter):
        self.__req_line = req.requestline
        # self._handle(req)
        try:
            self._handle(req)
            # 1
        except Exception as e:
            logger.error(f"{self.__req_line} -- Handle failed: {str(e)}")
            self._set_resp(500, str(e))
        except:
            logger.error(f"{self.__req_line} -- Handle failed: Unknow Error")
            self._set_resp(500, "Unknow Error")
        self._send_resp(req)
