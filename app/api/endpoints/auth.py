from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import APIKeyCookie
from ..dependencies.session import get_session

from ...models import Teacher
from ...schemas.auth import Login, ForgotPassword
from ...schemas.teacher import TeachersResponse

auth_router = APIRouter(prefix="/auth")
cookie = APIKeyCookie(name="token")


@auth_router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
)
async def login(
    response: Response,
    payload: Login = Depends(),
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    exist_teacher = await teacher.get_by(session, email=payload.email)
    if not exist_teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notog'ri email"
        )
    if not await exist_teacher.check_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Notogri parol"
        )
    token = await exist_teacher.generate_token()
    response.set_cookie("token", token)
    return {"detail": "Siz muvaffaqiyatli tizimga kirdingiz"}


@auth_router.get(
    "/me", status_code=status.HTTP_201_CREATED, response_model=TeachersResponse
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


arr = [4, 5, 1, 45, 12]
# @auth_router.post(
#     "/forgot-password",
#     status_code=status.HTTP_201_CREATED,
# )
# async def forgot_password(
#     response: Response,
#     payload: ForgotPassword = Depends(),
#     session: AsyncSession = Depends(get_session),
# ):
#     teacher = Teacher()
#     exist_teacher = await teacher.get_by(session, email=payload.email)
#     if not exist_teacher:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Notog'ri email"
#         )
#     if not await exist_teacher.check_password(payload.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Notogri parol"
#         )
#     token = await exist_teacher.generate_token()
#     response.set_cookie("token", token)
#     return
