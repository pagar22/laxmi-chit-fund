import os

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import (
    AccessSecretVersionResponse,
    SecretManagerServiceClient,
)

PROJECT_ID = os.getenv("PROJECT_ID", "laxmi-chit-fund-letsgetit")


def access_secret_manager(
    secret_id: str, version_id: str = "latest"
) -> AccessSecretVersionResponse:
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    try:
        secret_manager_client = SecretManagerServiceClient()
        resp = secret_manager_client.access_secret_version(name=name)
        return resp.payload.data.decode("UTF-8")
    except DefaultCredentialsError:
        raise PermissionError(
            "GCP user is not authenticated. To login run `gcloud auth application-default login`"
        )
