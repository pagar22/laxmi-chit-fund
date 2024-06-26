import base64
import json
import logging as __logging
import os

import firebase_admin
from app.internal.config import IS_EMULATOR_CONNECTED, access_secret_manager
from firebase_admin import credentials, firestore_async, storage

__storage_bucket_path = os.getenv(
    "STORAGE_BUCKET", "laxmi-chit-fund-letsgetit.appspot.com"
)

if IS_EMULATOR_CONNECTED:
    laxmi_chit_fund = firebase_admin.initialize_app()
else:
    __db_secret_path = os.getenv(
        "FIRESTORE_SERVICE_ACCOUNT", "firestore-service-account"
    )
    __service_account = base64.b64decode(access_secret_manager(__db_secret_path))
    __credentials = credentials.Certificate(json.loads(__service_account))
    laxmi_chit_fund = firebase_admin.initialize_app(__credentials)

# Services
db = firestore_async.client()
log = __logging.getLogger("uvicorn.app")
bucket = storage.bucket(__storage_bucket_path)
