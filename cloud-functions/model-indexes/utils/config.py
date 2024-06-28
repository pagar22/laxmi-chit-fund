import logging as __logging
import os

from google.cloud import storage

DATE_FORMAT = "%Y-%m-%d"
LOG = __logging.getLogger("cf.logger")

BUCKET_NAME = os.getenv("BUCKET_NAME")
LAXMI_API_URL = os.getenv("LAXMI_API_URL")
LAXMI_CUD_API_KEY = os.getenv("LAXMI_CUD_API_KEY", "j9t#-rUnDKzu.!A")

__storage_client = storage.Client()
bucket = __storage_client.bucket(BUCKET_NAME)
