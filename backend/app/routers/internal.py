from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["Health"])
async def get():
    return {"message": "pong!"}
