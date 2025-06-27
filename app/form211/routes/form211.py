from typing import Annotated

from db import get_async_db_session
from fastapi import APIRouter, Depends, HTTPException
from form211 import models
from form211.routes import schemas
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from timelog.models import Timelog as timelog_models
from user import models as user_models

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


@router.post("/{form211_id}/sign_in", summary="Sign in to a Form 211")
async def post_sign_in_form211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
    request_data: schemas.SignInForm211Request,
) -> schemas.SignInForm211Response:
    # Check that we are loading an active
    stmt = select(models.Form211).where(
        models.Form211.id == form211_id,
        models.Form211.deleted_at.is_(None),
    )

    form211 = (await db.execute(stmt)).scalar()

    if form211 is None:
        raise HTTPException(status_code=404, detail="Form 211 not found")

    # See if we can find a user based on the FSAR ID
    sar_id = request_data.sar_id
    if sar_id is not None:
        stmt = select(user_models.User).where(
            user_models.User.sar_id == sar_id,
            user_models.User.deleted_at.is_(None),
        )
        user = (await db.execute(stmt)).scalar()

        if user is None:
            sar_id = 0

    timelog = timelog_models(
        form211_id=form211.id,
        name=request_data.name,  # Name is required in the schema
        sar_id=sar_id or 0,
        resource_type="FSAR",
        created_by=request_data.created_by,
        departure_at=None,  # Start with empty departure time
    )

    db.add(timelog)
    await db.commit()
    await db.refresh(timelog)

    return schemas.SignInForm211Response(
        id=timelog.id,
        form211_id=timelog.form211_id,
        created_by=timelog.created_by,
        sar_id=timelog.sar_id,
        name=timelog.name,
        resource_type=timelog.resource_type,
        arrival_at=timelog.arrival_at,
        departure_at=timelog.departure_at,
    )


@router.put("/{form211_id}/sign_out/{sar_id}", summary="Sign out to a Form 211")
async def put_sign_out_form211(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
    sar_id: int,
) -> schemas.SignOutForm211Response:
    # Check that we are loading an active
    stmt = select(models.Form211).where(
        models.Form211.id == form211_id,
        models.Form211.deleted_at.is_(None),
    )

    form211 = (await db.execute(stmt)).scalar()

    if form211 is None:
        raise HTTPException(status_code=404, detail="Form 211 not found")

    # See if we can find a user based on the FSAR ID
    stmt = select(user_models.User).where(
        user_models.User.sar_id == sar_id,
        user_models.User.deleted_at.is_(None),
    )
    user = (await db.execute(stmt)).scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="SAR ID not found")

    # find the timelog entry that is not already signed out.
    stmt = select(timelog_models).where(
        timelog_models.form211_id == form211_id,
        timelog_models.sar_id == sar_id,
        timelog_models.departure_at.is_(None),
        timelog_models.deleted_at.is_(None),
    )

    timelog = (await db.execute(stmt)).scalar()
    if timelog is None:
        raise HTTPException(status_code=404, detail="User not checked in.")

    timelog.departure_at = func.now()
    await db.commit()
    await db.refresh(timelog)

    return schemas.SignInForm211Response(
        id=timelog.id,
        form211_id=timelog.form211_id,
        created_by=timelog.created_by,
        sar_id=timelog.sar_id,
        name=timelog.name,
        resource_type=timelog.resource_type,
        arrival_at=timelog.arrival_at,
        departure_at=timelog.departure_at,
    )


@router.get("/{form211_id}/arrivals", summary="Retrieve a form 211")
async def get_form211_arrivals(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    form211_id: int,
) -> schemas.ListTimelogResponse:
    count_stmt = select(func.count(timelog_models.id)).where(
        timelog_models.form211_id == form211_id, timelog_models.deleted_at.is_(None)
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = select(
        timelog_models.id,
        timelog_models.form211_id,
        timelog_models.created_by,
        timelog_models.sar_id,
        timelog_models.name,
        timelog_models.resource_type,
        timelog_models.arrival_at,
        timelog_models.departure_at,
        timelog_models.created_at,
        timelog_models.updated_at,
    ).where(
        timelog_models.form211_id == form211_id, timelog_models.deleted_at.is_(None)
    )

    result_rows = (await db.execute(stmt)).all()

    return schemas.ListTimelogResponse(
        count=count_result,
        items=[
            schemas.ListTimelogResponseItem(
                id=row.id,
                form211_id=row.form211_id,
                sar_id=row.sar_id,
                created_by=row.created_by,
                name=row.name,
                resource_type=row.resource_type,
                arrival_at=row.arrival_at,
                departure_at=row.departure_at,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in result_rows
        ],
    )
