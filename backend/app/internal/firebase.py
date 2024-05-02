import base64
import json
import os

import firebase_admin
from app.internal.config import access_secret_manager
from firebase_admin import credentials, firestore_async

__service_account = os.getenv("FIRESTORE_SERVICE_ACCOUNT", "firestore-service-account")
__service_account_json = base64.b64decode(access_secret_manager(__service_account))
__credentials = credentials.Certificate(json.loads(__service_account_json))
laxmi_chit_fund = firebase_admin.initialize_app(__credentials)

db = firestore_async.client()
