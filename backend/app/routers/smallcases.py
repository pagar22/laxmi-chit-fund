from app.daos.smallcases import SmallcaseDAO
from app.schemas.smallcases import MonthlySmallcaseStatisticsBase, SmallcaseBase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
smallcaseDAO = SmallcaseDAO()


@router.get("/{id}")
async def get(id: str):
    smallcase = await smallcaseDAO.get(id)
    if smallcase:
        return smallcase
    raise HTTPException(status_code=404, detail="Smallcase not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(smallcase: SmallcaseBase):
    await smallcaseDAO.create(smallcase, smallcase.id)


@router.post("/{id}/statistics", status_code=status.HTTP_201_CREATED)
async def create_statistics(id: str, monthly_stats: MonthlySmallcaseStatisticsBase):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_statistics(monthly_stats, id)
