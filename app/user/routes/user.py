from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db_session
from user import models
from user.routes import schemas

# /api/v1/user
router = APIRouter()

@router.post("", summary="Create a new user")
async def post_create_user(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    request_data: schemas.CreateUserRequest,
) -> schemas.CreateUserResponse:
    user = models.User(name=request_data.name, email=request_data.email, resource_type=request_data.resource_type)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return schemas.CreateUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        resource_type=user.resource_type,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.get("/{user_id}", summary="Rrtrieve a user")
async def get_user(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    user_id: int,
) -> schemas.RetrieveUserResponse:
    stmt = select(
        models.User.id,
        models.User.name,
        models.User.email,
        models.User.resource_type,
        models.User.created_at,
        models.User.updated_at
    ).where(
        models.User.id == user_id,
        models.User.deleted_at.is_(None)
    )
    result_row = (await db.execute(stmt)).first()

    if result_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    mapped_row = result_row._mapping
    return schemas.RetrieveUserResponse(
        id=mapped_row[models.User.id],
        name=mapped_row[model.User.name],
        email=mapped_row[model.User.email],
        resource_type=mapped_row[model.User.resource_type],
        created_at=mapped_row[model.User.created_at],
        updated_at=mapped_row[model.User.updated_at],
    )

@router.get("", summary="List all users")
async def get_users(
    db: Annotated[AsyncSession, Depends(get_async_db_session)]
) -> schemas.ListUsersResponse:
    count_stmt = select(func.count(models.User.id)).where(
        models.User.deleted_at.is_(None)
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(
            models.User.id,
            models.User.name,
            models.User.email,
            models.User.resource_type,
            models.User.created_at,
            models.User.updated_at
        ).where(
            models.User.deleted_at.is_(None)
        ).order_by(models.User.created_at.desc())
    )

    result_rows = (await db.execute(stmt)).all()

    return schemas.ListUsersResponse(
        count=count_result,
        items=[
            schemas.ListUsersResponseItem(
                id=row.id,
                name=row.name,
                email=row.email,
                resource_type=row.resource_type,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            for row in result_rows
        ]
    )


@router.put("/{user_id}", summary="Update a user")
async def put_user(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    user_id: int,
    request_data: schemas.UpdateUserRequest
) -> schemas.UpdateUserResponse:
    stmt = select(models.User).where(
        models.User.id == user_id,
        models.User.deleted_at.is_(None)
    )

    user = (await db.execute(stmt)).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = request_data.name
    user.resource_type = request_data.resource_type

    await db.commit()
    await db.refresh(user)

    return schemas.UpdateUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        resource_type=user.resource_type,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.delete("/{user_id}", summary="Delete a user", status_code=204)
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    user_id: int,
) -> None:
    stmt = select(models.User).where(
        models.User.id == user_id,
        models.User.deleted_at.is_(None),
    )
     
    user = (await db.execute(stmt)).scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted_at = func.now()
    await db.commit()
    await db.refresh(user)
    return None