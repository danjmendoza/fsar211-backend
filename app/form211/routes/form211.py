from typing import Annotated

from db import get_async_db_session
from fastapi import APIRouter, Depends, HTTPException
from form211 import models
from form211.routes import schemas
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# /api/v1/user
router = APIRouter()


@router.post("", summary="Create a new form 211")
async def post_create_form211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    request_data: schemas.CreateForm211Request,
) -> schemas.CreateForm211Response:
    form211 = models.Form211(
        name=request_data.name,
        created_by=request_data.created_by,
        operational_period=request_data.operational_period,
    )
    db.add(form211)
    await db.commit()
    await db.refresh(form211)

    return schemas.CreateForm211Response(
        id=form211.id,
        created_by=form211.created_by,
        name=form211.name,
        operational_period=form211.operational_period,
        created_at=form211.created_at,
        updated_at=form211.updated_at,
        closed_at=form211.closed_at,
    )


@router.get("/{form211_id}", summary="Retrieve a form 211")
async def get_form211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
) -> schemas.RetrieveForm211Response:
    stmt = select(
        models.Form211.id,
        models.Form211.created_by,
        models.Form211.name,
        models.Form211.operational_period,
        models.Form211.created_at,
        models.Form211.updated_at,
        models.Form211.closed_at,
    ).where(models.Form211.id == form211_id, models.Form211.deleted_at.is_(None))
    result_row = (await db.execute(stmt)).first()

    if result_row is None:
        raise HTTPException(status_code=404, detail="Form 211 not found")

    mapped_row = result_row._mapping
    return schemas.RetrieveForm211Response(
        id=mapped_row[models.Form211.id],
        created_by=mapped_row[models.Form211.created_by],
        name=mapped_row[models.Form211.name],
        operational_period=mapped_row[models.Form211.operational_period],
        created_at=mapped_row[models.Form211.created_at],
        updated_at=mapped_row[models.Form211.updated_at],
        closed_at=mapped_row[models.Form211.closed_at],
    )


@router.get("", summary="List all Form 211")
async def get_form211s(
    db: Annotated[AsyncSession, Depends(get_async_db_session)]
) -> schemas.ListForm211Response:
    count_stmt = select(func.count(models.Form211.id)).where(
        models.Form211.deleted_at.is_(None)
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(
            models.Form211.id,
            models.Form211.created_by,
            models.Form211.name,
            models.Form211.operational_period,
            models.Form211.created_at,
            models.Form211.updated_at,
            models.Form211.closed_at,
        )
        .where(models.Form211.deleted_at.is_(None))
        .order_by(models.Form211.created_at.desc())
    )

    result_rows = (await db.execute(stmt)).all()

    return schemas.ListForm211Response(
        count=count_result,
        items=[
            schemas.ListForm211ResponseItem(
                id=row.id,
                created_by=row.created_by,
                name=row.name,
                operational_period=row.operational_period,
                created_at=row.created_at,
                updated_at=row.updated_at,
                closed_at=row.closed_at,
            )
            for row in result_rows
        ],
    )


@router.put("/{form211_id}", summary="Update a Form 211")
async def put_211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
    request_data: schemas.UpdateForm211Request,
) -> schemas.UpdateForm211Response:
    stmt = select(models.Form211).where(
        models.Form211.id == form211_id, models.Form211.deleted_at.is_(None)
    )

    form211 = (await db.execute(stmt)).scalar()
    if form211 is None:
        raise HTTPException(status_code=404, detail="Form 211 not found")

    form211.name = request_data.name

    await db.commit()
    await db.refresh(form211)

    return schemas.UpdateForm211Response(
        id=form211.id,
        created_by=form211.created_by,
        name=form211.name,
        operational_period=form211.operational_period,
        created_at=form211.created_at,
        updated_at=form211.updated_at,
        closed_at=form211.closed_at,
    )


@router.delete("/{form211_id}", summary="Delete a Form 211", status_code=204)
async def delete_form211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
) -> None:
    stmt = select(models.Form211).where(
        models.Form211.id == form211_id,
        models.Form211.deleted_at.is_(None),
    )

    form211 = (await db.execute(stmt)).scalar()

    if form211 is None:
        raise HTTPException(status_code=404, detail="From 211 not found")

    form211.deleted_at = func.now()
    await db.commit()
    await db.refresh(form211)
    return None
