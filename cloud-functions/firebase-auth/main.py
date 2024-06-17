import logging

import bcrypt
import functions_framework
from firebase_admin import auth, firestore, initialize_app
from flask import Request

app = initialize_app()
db = firestore.client(app)
log = logging.getLogger("cloud-functions.error")


@functions_framework.http
def main(request: Request) -> str:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    }
    if request.method == "OPTIONS":
        log.info("🫡 Responding to CORS")
        return ("", 204, headers)

    data: dict = request.get_json().get("data")
    device_id = data.get("deviceId")
    password = data.get("password")
    if not device_id or not password:
        return "bad_request", 400

    try:
        query = db.collection("devices").where("device_id", "==", device_id).get()
        if not query:
            hashed = hash_password(password)
            payload = {"device_id": device_id, "password": hashed}
            user = db.collection("devices").add(payload)
            uid = user[1].id
        else:
            device = query[0]
            hashed = device.to_dict()["password"]
            if not verify_password(password, hashed):
                log.error("🙏 Incorrect password")
                return "incorrect_password", 401
            uid = device.id

        custom_token = auth.create_custom_token(uid)
        return ({"data": custom_token.decode("utf-8")}, 200, headers)

    except Exception as e:
        log.error(f"🚨 Error creating custom token: {e}")
        return "unauthorized", 403


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
