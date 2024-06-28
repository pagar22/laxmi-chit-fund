from datetime import datetime
from typing import List, Optional

from app.daos.smallcases import SmallcaseDAO
from app.schemas.smallcases import (
    IndexBase,
    SmallcaseBase,
    SmallcaseConstituentsBase,
    SmallcaseIndexesBase,
    SmallcaseStatisticsBase,
)
from app.utils.dates import dateparse, datestr, validate_date_range
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


@router.get("/{id}/constituents", response_model=Optional[SmallcaseConstituentsBase])
async def get_constituents(id: str, date: str):
    date = datestr(date, full_path=True)
    latest = dateparse(date) >= datetime.now().date()
    constituents = await smallcaseDAO.get_constituents(id, date, latest=latest)
    if not constituents:
        raise HTTPException(status_code=404, detail="Constituents not found")
    return constituents


@router.get(
    "/{id}/constituents/stream",
    response_model=Optional[List[SmallcaseConstituentsBase]],
)
async def get_constituents_stream(id: str):
    constituents = await smallcaseDAO.get_constituents_stream(id)
    if not constituents:
        raise HTTPException(status_code=404, detail="Constituents not found")
    return constituents


@router.get("/{id}/indexes", response_model=dict[str, IndexBase])
async def get_indexes(id: str, start_date: str, end_date: str):
    validate_date_range(start_date, end_date, max_days=365 * 5)
    indexes = await smallcaseDAO.get_indexes(id, start_date, end_date)
    if not indexes:
        raise HTTPException(status_code=404, detail="Indexes not found")
    return indexes


@router.get("/{id}/statistics", response_model=SmallcaseStatisticsBase)
async def get_statistics(id: str, date: str):
    date = datestr(date)
    statistics = await smallcaseDAO.get_statistics(id, date)
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics not found")
    return statistics


@router.post("/", status_code=201)
async def create(smallcase: SmallcaseBase):
    await smallcaseDAO.create(smallcase, smallcase.id)


@router.post("/{id}/constituents", status_code=201)
async def create_constituents(id: str, constituents: SmallcaseConstituentsBase):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_constituents(id, constituents)


@router.post("/{id}/indexes", status_code=201)
async def create_indexes(id: str, indexes: SmallcaseIndexesBase):
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_indexes(id, indexes)


@router.post("/{id}/statistics", status_code=201)
async def create_statistics(id: str, monthly_stats: SmallcaseStatisticsBase, date: str):
    date = datestr(date)
    smallcase = await smallcaseDAO.get(id)
    if not smallcase:
        raise HTTPException(status_code=404, detail="Smallcase not found")

    await smallcaseDAO.create_statistics(id, monthly_stats, date)
