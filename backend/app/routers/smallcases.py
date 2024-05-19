from app.daos.smallcases import SmallcaseDAO
from app.schemas.smallcases import (
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import datestr
from fastapi import APIRouter, HTTPException

router = APIRouter()
smallcaseDAO = SmallcaseDAO()


@router.get("/")
async def list():
    return await smallcaseDAO.stream()


@router.get("/{id}")
async def get(id: str):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")
    return smallcase


@router.post("/", status_code=201)
async def create(smallcase: SmallcaseBase):
    await smallcaseDAO.create(smallcase, smallcase.id)


@router.get("/{id}/constituents")
async def get_constituents(id: str, date: str):
    date = datestr(date)
    constituents = await smallcaseDAO.get_constituents(id, date)
    if not constituents:
        raise HTTPException(status_code=404, detail="Constituents not found")
    return constituents


@router.post("/{id}/constituents", status_code=201)
async def create_constituents(id: str, constituents: SmallcaseConstituentsBase):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_constituents(id, constituents)


@router.get("/{id}/statistics")
async def get_statistics(id: str, date: str):
    date = datestr(date)
    statistics = await smallcaseDAO.get_statistics(id, date)
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics not found")
    return statistics


@router.post("/{id}/statistics", status_code=201)
async def create_statistics(id: str, monthly_stats: SmallcaseStatisticsBase, date: str):
    date = datestr(date)
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_statistics(id, monthly_stats, date)
