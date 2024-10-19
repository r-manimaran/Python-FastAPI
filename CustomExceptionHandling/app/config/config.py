import sys
import logging

from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from config.logging import InterceptHandler
config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.0.1"
DEBUG = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
SECRET_KEY = config("SECRET_KEY", cast=Secret)
PROJECT_NAME = config("PROJECT_NAME", default="FastAPI example application")

#logging
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(levelname)s %(asctime)s %(name)s %(message)s",
    handlers=[
        InterceptHandler(level=LOGGING_LEVEL)
    ],
)