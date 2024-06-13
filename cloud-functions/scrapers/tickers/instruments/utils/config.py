import logging

from google.cloud import storage

__storage_client = storage.Client()

LOG = logging.getLogger("cloud-functions.error")
BUCKET = __storage_client.bucket("laxmi-chit-fund-letsgetit.appspot.com")
LAXMI_URL = "http://localhost:2000"
# LAXMI_URL = "https://laxmi-chit-fund-xgqm3fv7ua-ew.a.run.app"
