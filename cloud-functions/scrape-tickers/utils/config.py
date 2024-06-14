import logging as __logging
import os

from google.cloud import storage
from google.cloud.secretmanager import SecretManagerServiceClient

__storage_client = storage.Client()


def access_secret_manager(secret_id: str, version_id: str = "latest") -> str:
    secret_client = SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = secret_client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        log.error(f"Error accessing secret {secret_id}", e)
        raise PermissionError("🚨 Environment not authenticated.")


PROJECT_ID = os.getenv("PROJECT_ID", "laxmi-chit-fund-letsgetit")
BUCKET_NAME = os.getenv("STORAGE_BUCKET", "laxmi-chit-fund-letsgetit.appspot.com")
LAXMI_API_URL = os.getenv("LAXMI_API_URL", "http://localhost:2000")
LAXMI_CUD_API_KEY = access_secret_manager("CUD_API_KEY", "latest")

log = __logging.getLogger("cloud-functions.error")
bucket = __storage_client.bucket(BUCKET_NAME)
