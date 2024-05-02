from app.internal.firebase import db
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get():
    x = await db.document("tickers/HINDALCO").get()
    return x.to_dict()


@router.post("/")
def create():
    return {"data": "posted"}
