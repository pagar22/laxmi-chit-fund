# Laxmi Chit Fund Backend

## Tech Dependencies

- Python >= 3.11 🫶
- Docker Desktop
- Google Cloud CLI

## Build

The app can be built locally in two ways:

**_1. Emulating Firestore (Recommended)_** 😶‍🌫️

```
docker compose up --build
```

Go to [localhost:2000](http://localhost:2000/docs)

**_2. Connecting to the dev Firestore db_** 🙏

Create venv and install dependencies

```
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

Login to GCP via Application Default Credentials (ADC)

```
gcloud auth application-default login
```

Start uvicorn server

```
uvicorn app.main:app --port 8000 --reload
```

Go to [localhost:8000](http://localhost:8000/docs)

## Testing

🚨 Always make sure you're connected to the emulator when testing locally! The tests will not start if they don't detect an emulator, but better safe than sorry.

1. Build the test container (once only).

```
docker compose -f docker-compose-tests.yaml build
```

2. Run tests. Fill PYTEST_ARGS as required.

```
docker compose -f docker-compose-tests.yaml run -e PYTEST_ARGS="" tests
```

## Deploying

Manually deploy BE to GCP Cloud Run

```
gcloud run deploy laxmi-chit-fund --source .
```

Always clean up older revisions on GAR to reduce artifact registry costs.
