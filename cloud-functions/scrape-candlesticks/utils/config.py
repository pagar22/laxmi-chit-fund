import logging as __logging
import os

PROJECT_ID = os.getenv("PROJECT_ID")
UPSTOX_API_URL = os.getenv("UPSTOX_API_URL")
LAXMI_API_URL = os.getenv("LAXMI_API_URL")
LAXMI_CUD_API_KEY = os.getenv("LAXMI_CUD_API_KEY")

log = __logging.getLogger("cloud-functions.error")
