from app.daos.smallcases import SmallcaseDAO
from app.schemas.smallcases import (
    IndexBase,
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseIndexesBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import datestr, get_days_between_dates
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


@router.get("/{id}/indexes", response_model=dict[str, IndexBase])
async def get_indexes(id: str, start_date: str, end_date: str):
    start_date = datestr(start_date)
    end_date = datestr(end_date)
    days = get_days_between_dates(start_date, end_date)
    if days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    indexes = await smallcaseDAO.get_indexes(id, start_date, end_date)
    if not indexes:
        raise HTTPException(status_code=404, detail="Indexes not found")
    return indexes


@router.post("/{id}/indexes", status_code=201)
async def create_indexes(id: str, indexes: SmallcaseIndexesBase, date: str):
    date = datestr(date)
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_indexes(id, indexes, date)


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
