from app.daos.smallcases import SmallcaseDAO
from app.schemas.smallcases import SmallcaseBase, SmallcaseStatisticsBase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
smallcaseDAO = SmallcaseDAO()


@router.get("/{id}")
async def get(id: str):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")
    return smallcase


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(smallcase: SmallcaseBase):
    await smallcaseDAO.create(smallcase, smallcase.id)


@router.post("/{id}/statistics", status_code=status.HTTP_201_CREATED)
async def create_statistics(id: str, monthly_stats: SmallcaseStatisticsBase):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_statistics(monthly_stats, id)
