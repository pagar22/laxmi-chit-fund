import base64
import json
import os

import firebase_admin
from app.internal.config import access_secret_manager
from firebase_admin import credentials, firestore_async, storage

__db_secret_path = os.getenv("FIRESTORE_SERVICE_ACCOUNT", "firestore-service-account")
__storage_bucket_path = os.getenv(
    "STORAGE_BUCKET", "laxmi-chit-fund-letsgetit.appspot.com"
)

__service_account = base64.b64decode(access_secret_manager(__db_secret_path))
__credentials = credentials.Certificate(json.loads(__service_account))
laxmi_chit_fund = firebase_admin.initialize_app(__credentials)


# Services
db = firestore_async.client()
bucket = storage.bucket(__storage_bucket_path)
