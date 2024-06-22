CERTIFICATE_PATH = ''
USE_TLS          = False
PORT             = 80
WEB_DIST         = "../web/dist"

DATABASE_CONF    = {
    "host": "wsl.local",
    "port": 5432,
    "user": "postgres",
    "password": "a",
    "database": "pttk",
}

from utils.utils import logger
LOG_LEVEL       = logger.INFO
LOG_FILE        = None
