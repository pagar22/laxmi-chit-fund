from app.routers import smallcases, tickers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# TODO: Update origins to FE URL
origins = ["*", "http://localhost:19006"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", tags=["Health"])
def ping():
    return {"data": "pong!"}


app.include_router(tickers.router, prefix="/tickers", tags=["Tickers"])
app.include_router(smallcases.router, prefix="/smallcases", tags=["Smallcases"])
