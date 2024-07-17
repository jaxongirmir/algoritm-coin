from __future__ import annotations
from typing import List, Union
from uuid import UUID
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies.session import get_session
from schemas.teacher import (
    TeacherCreate,
    TeacherResponse,
    TeacherWithGroupsResponse,
    TeacherUpdate,
)
from models import Teacher


teacher_router = APIRouter(prefix="/teacher")


@teacher_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TeacherResponse,
)
async def create_teacher(
    payload: TeacherCreate,
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(email=payload.email)
    if await teacher.get_with_groups(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bu email {teacher.fullname} ga tegishli",
        )
    await payload.hach_password()
    teacher = Teacher(
        _password=payload._password,
        **payload.model_dump(
            exclude={"password"},
        ),
    )
    await teacher.save(session)
    return teacher


@teacher_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[TeacherWithGroupsResponse] | TeacherWithGroupsResponse,
)
async def get_teacher(
    id: UUID | None = None,
    email: EmailStr | None = None,
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(id=id, email=email)
    if id or email:
        await teacher.get_with_groups_and_students(session)
        return teacher
    else:
        return await teacher.get_all_with_groups_and_students(session)


@teacher_router.put("/", status_code=status.HTTP_200_OK)
async def update_teacher(
    payload: TeacherUpdate,
    session: AsyncSession = Depends(get_session),
):

    teacher = Teacher(
        id=payload.teacher_id,
    )
    return await teacher.update(
        session,
        **payload.model_dump(exclude_none=True, exclude={"teacher_id", "password"}),
    )


@teacher_router.delete("/", status_code=status.HTTP_200_OK)
async def delet_teacher(
    teacher_id,
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(id=teacher_id)
    await teacher.delete(session)
    return {"message": "teacher deleted"}
