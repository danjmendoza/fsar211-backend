from typing import Annotated

from db import get_async_db_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from timelog import models
from timelog.routes import schemas

# /api/v1/user
router = APIRouter()


@router.post("", summary="Create a new time entry")
async def post_create_timelog(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    request_data: schemas.CreateTimelogRequest,
) -> schemas.CreateTimelogResponse:
    timelog = models.Timelog(
        form211_id=request_data.form211_id,
        name=request_data.name,
        created_by=request_data.created_by,
        sar_id=request_data.sar_id,
        resource_type=request_data.resource_type,
        arrival_at=request_data.arrival_at,
        departure_at=request_data.departure_at,
    )
    db.add(timelog)
    await db.commit()
    await db.refresh(timelog)

    return schemas.CreateTimelogResponse(
        id=timelog.id,
        form211_id=timelog.form211_id,
        created_by=timelog.created_by,
        name=timelog.name,
        sar_id=timelog.sar_id,
        resource_type=timelog.resource_type,
        arrival_at=timelog.arrival_at,
        departure_at=timelog.departure_at,
        created_at=timelog.created_at,
        updated_at=timelog.updated_at,
    )


@router.get("/{timelog_id}", summary="Retrieve a time entry")
async def get_timelog(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    timelog_id: int,
) -> schemas.RetrieveTimelogResponse:
    stmt = select(
        models.Timelog.id,
        models.Timelog.created_by,
        models.form211_id,
        models.Timelog.name,
        models.Timelog.sar_id,
        models.Timelog.resource_type,
        models.Timelog.arrival_at,
        models.Timelog.departure_at,
        models.Timelog.created_at,
        models.Timelog.updated_at,
    ).where(models.Timelog.id == timelog_id, models.Timelog.deleted_at.is_(None))
    result_row = (await db.execute(stmt)).first()

    if result_row is None:
        raise HTTPException(status_code=404, detail="Timelog not found")

    mapped_row = result_row._mapping
    return schemas.RetrieveTimelogResponse(
        id=mapped_row[models.Timelog.id],
        form211_id=mapped_row[models.Timelog.form211_id],
        created_by=mapped_row[models.Timelog.created_by],
        name=mapped_row[models.Timelog.name],
        sar_id=mapped_row[models.Timelog.sar_id],
        resource_type=mapped_row[models.Timelog.resource_type],
        arrival_at=mapped_row[models.Timelog.arrival_at],
        departure_at=mapped_row[models.Timelog.departure_at],
        created_at=mapped_row[models.Timelog.created_at],
        updated_at=mapped_row[models.Timelog.updated_at],
    )


@router.get("", summary="List all Time Entries")
async def get_timelogs(
    db: Annotated[AsyncSession, Depends(get_async_db_session)]
) -> schemas.ListTimelogResponse:
    count_stmt = select(func.count(models.Timelog.id)).where(
        models.Timelog.deleted_at.is_(None)
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(
            models.Timelog.id,
            models.Timelog.created_by,
            models.Timelog.form211_id,
            models.Timelog.name,
            models.Timelog.sar_id,
            models.Timelog.resource_type,
            models.Timelog.arrival_at,
            models.Timelog.departure_at,
            models.Timelog.created_at,
            models.Timelog.updated_at,
        )
        .where(models.Timelog.deleted_at.is_(None))
        .order_by(models.Timelog.created_at.desc())
    )

    result_rows = (await db.execute(stmt)).all()

    return schemas.ListTimelogResponse(
        count=count_result,
        items=[
            schemas.ListTimelogResponseItem(
                id=row.id,
                created_by=row.created_by,
                form211_id=row.form211_id,
                name=row.name,
                sar_id=row.sar_id,
                resource_type=row.resource_type,
                arrival_at=row.arrival_at,
                departure_at=row.departure_at,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in result_rows
        ],
    )


@router.put("/{timelog_id}", summary="Update a Time Entry")
async def put_timelog(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    timelog_id: int,
    request_data: schemas.UpdateTimelogRequest,
) -> schemas.UpdateTimelogResponse:
    stmt = select(models.Timelog).where(
        models.Timelog.id == timelog_id, models.Timelog.deleted_at.is_(None)
    )

    timelog = (await db.execute(stmt)).scalar()
    if timelog is None:
        raise HTTPException(status_code=404, detail="Timelog not found")

    timelog.name = request_data.name

    await db.commit()
    await db.refresh(timelog)

    return schemas.UpdateTimelogResponse(
        id=timelog.id,
        form211_id=timelog.form211_id,
        sar_id=timelog.sar_id,
        created_by=timelog.created_by,
        name=timelog.name,
        resource_type=timelog.resource_type,
        arrival_at=timelog.arrival_at,
        departure_at=timelog.departure_at,
        created_at=timelog.created_at,
        updated_at=timelog.updated_at,
    )


@router.delete("/{timelog_id}", summary="Delete a Time Entry", status_code=204)
async def delete_timelog(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    timelog_id: int,
) -> None:
    stmt = select(models.Timelog).where(
        models.Timelog.id == timelog_id,
        models.Timelog.deleted_at.is_(None),
    )

    timelog = (await db.execute(stmt)).scalar()

    if timelog is None:
        raise HTTPException(status_code=404, detail="Timelog not found")

    timelog.deleted_at = func.now()
    await db.commit()
    await db.refresh(timelog)
    return None
