import logging

import bcrypt
import functions_framework
from firebase_admin import auth, firestore, initialize_app
from flask import Request
from google.cloud.firestore_v1.base_query import FieldFilter

app = initialize_app()
db = firestore.client(app)
log = logging.getLogger("cloud-functions.error")


@functions_framework.http
def main(request: Request) -> str:
    try:
        data: dict = request.get_json()["data"]
        device_id = data["deviceId"]
        password = data["password"]
    except Exception as e:
        log.error(f"🚨 Error parsing request: {e}")
        return "bad_request", 400

    try:
        collection = db.collection("devices")
        docs = collection.where(filter=FieldFilter("deviceId", "==", device_id)).get()
        if not docs:
            hashed = hash_password(password)
            doc = collection.add({"deviceId": device_id, "password": hashed})
            uid = doc[1].id
        else:
            device = docs[0]
            hashed = device.to_dict()["password"]
            if not verify_password(password, hashed):
                log.error("🙏 Incorrect password")
                return "unauthorized", 403
            uid = device.id

        log.info(f"🔑 Auth successful. Creating token for {uid}")
        custom_token = auth.create_custom_token(uid)
        return {"data": custom_token.decode("utf-8")}, 200

    except Exception as e:
        log.error(f"🚨 Error creating custom token: {e}")
        return "unauthenticated", 401


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
