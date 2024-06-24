import os

import requests
from google.api_core.exceptions import PermissionDenied
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import (
    AccessSecretVersionResponse,
    SecretManagerServiceClient,
)


def __is_emulator_connected(host, port):
    try:
        resp = requests.get(f"http://{host}:{port}", timeout=3)
        demo_project = os.getenv("GCLOUD_PROJECT") == "demo-laxmi-chit-fund-letsgetit"
        connected = resp.status_code == 200 and demo_project
    except requests.exceptions.RequestException:
        connected = False
    finally:
        if connected:
            print(f"💚 Emulator connected")
            os.environ["FIRESTORE_EMULATOR_HOST"] = f"{host}:{port}"
        else:
            print(f"💛 Emulator NOT connected")
            os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
        return connected


def access_secret_manager(
    secret_id: str, version_id: str = "latest"
) -> AccessSecretVersionResponse:
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    try:
        secret_manager_client = SecretManagerServiceClient()
        resp = secret_manager_client.access_secret_version(name=name)
        return resp.payload.data.decode("UTF-8")
    except (DefaultCredentialsError, PermissionDenied):
        raise PermissionError(
            "GCP user is not authenticated. To login run `gcloud auth application-default login`"
        )


PROJECT_ID = os.getenv("PROJECT_ID", "laxmi-chit-fund-letsgetit")
IS_EMULATOR_CONNECTED = __is_emulator_connected("firestore-emulator", 2021)
