import logging as __logging
import os

DATE_FORMAT = "%Y-%m-%d"
LOG = __logging.getLogger("cf.logger")

LAXMI_API_URL = os.getenv("LAXMI_API_URL")
LAXMI_CUD_API_KEY = os.getenv("LAXMI_CUD_API_KEY", "j9t#-rUnDKzu.!A")


# Exceptions
class TickerNotFoundException(Exception):
    pass
