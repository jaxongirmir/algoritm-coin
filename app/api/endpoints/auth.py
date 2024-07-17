from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from fastapi.responses import Response
from api.dependencies.session import get_session
from models import Teacher
from schemas.auth import Login, ForgotPassword, ChangePassword
from schemas.teacher import TeacherWithGroupsResponse

auth_router = APIRouter(prefix="/auth")
cookie = APIKeyCookie(name="token")


@auth_router.get(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
)
async def login(
    response: Response,
    payload: Login = Depends(),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(email=payload.email)
    exist_teacher = await teacher.get_with_groups(session)
    if not exist_teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notog'ri email"
        )
    if not await exist_teacher.check_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notogri parol"
        )
    token = await exist_teacher.generate_token()

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
    )
    return {"detail": "Siz muvaffaqiyatli tizimga kirdingiz"}


@auth_router.get(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    response: Response,
    token: str = Depends(cookie),
):
    response.delete_cookie(key="token")
    return {"detail": "Siz tizimdan muvaffaqiyatli chiqdingiz"}


@auth_router.get(
    "/me",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TeacherWithGroupsResponse,
)
async def me(
    token: str = Depends(cookie),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    if not await teacher.verify_token(token):
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )

    await teacher.get_with_groups_and_students(session)
    return teacher


@auth_router.get(
    "/forgot-password",
    status_code=status.HTTP_205_RESET_CONTENT,
)
async def forgot_password(
    payload: ForgotPassword = Depends(),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher(email=payload.email)
    exist_teacher = await teacher.get_with_groups(session)
    if not exist_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notog'ri email"
        )
    token = await exist_teacher.generate_token()
    return


@auth_router.put(
    "/password",
    status_code=status.HTTP_200_OK,
)
async def change_password(
    payload: ChangePassword,
    token: str = Depends(cookie),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    if not await teacher.verify_token(token):
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )
    await teacher.get(session)
    if not await teacher.check_password(payload.old_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Eski parol notogri"
        )
    await teacher.update(session)
    return
