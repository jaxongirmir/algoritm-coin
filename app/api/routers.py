from fastapi.routing import APIRouter
from .endpoints.auth import auth_router
from .endpoints.teacher import teacher_router
from .endpoints.group import group_router
from .endpoints.student import student_router
from .endpoints.settings import settings_router


api_routers = APIRouter()
api_routers.include_router(auth_router, tags=["AUTH"])
api_routers.include_router(teacher_router, tags=["TEACHER"])
api_routers.include_router(group_router, tags=["GROUP"])
api_routers.include_router(student_router, tags=["STUDENT"])
api_routers.include_router(settings_router, tags=["SETTINGS"])
