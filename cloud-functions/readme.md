## Laxmi Chit Fund Cloud Functions 😶‍🌫️

Cloud Functions are a great way to write stateless, componentised pieces of code that can be triggered at set intervals by predefined jobs with the benefit of added security.

Laxmi Chit Fund leverages cloud functions to write repeatedly exectuable mini-pieces of code without adding load to the main BE API and maintaining a clear seperation of concerns.

### Functions

At the moment we have the following functions:

    Scrapers

        1. Tickers (Market Instruments)
        2. Candlesticks (Historical price data for tickers)
        3. Smallcases (Smallcase details and statistics)

    Models
        1. Kelly (To find a Kelly Optimal Smallcase)
        2. Indexes (To find custom index returns of Smallcases)

    Auth
        1. Firebase Auth (To make a custom JWT token to authenticate a user on the FE)

### Develop Locally

Note: Functions interact with the development database. This is expected, but please be cautious.

1. Login to GCP via Application Default Credentials (ADC)

```
gcloud auth application-default login
```

2. cd into the function repo you want to run (eg. `scrape-tickers`)

```
cd cloud-functions/scrape-tickers
```

3. Start the function

```
PYTHONDONTWRITEBYTECODE=1 functions-framework --target=main --debug
```

4. Send a normal cURL request to 8080 to invoke

```
curl --location 'localhost:8080' \
--header 'Content-Type: application/json' \
--data '{"exchange_token":"100"}'
```

### Deploy

Most functions have a cloudbuild.yaml file. This file is used by triggers setup on Cloud Build and invoked only when changes are made to the directory of the function.

If manual deployment is needed for any reason, the cloudbuild file essentially describes all the CLI params.

### Future Works

Several ideas are planned for functions in the future including

1. Creating a shared private pip package with configs and utils which can be reused by all functions.
2. With Firebase auth setup on the frontend, the functions can be setup to be only invoked by admin users and forward the admin's JWT token, removing the CUD API Key entirely.
3. Setup background tasks to automatically invoke functions from a secure server-side environment.
