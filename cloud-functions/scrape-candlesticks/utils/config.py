import logging as __logging
import os

from google.cloud import storage

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("STORAGE_BUCKET")
UPSTOX_API_URL = os.getenv("UPSTOX_API_URL")
LAXMI_API_URL = os.getenv("LAXMI_API_URL")
LAXMI_CUD_API_KEY = os.getenv("LAXMI_CUD_API_KEY")

__storage_client = storage.Client()
log = __logging.getLogger("cloud-functions.error")
bucket = __storage_client.bucket(BUCKET_NAME)
