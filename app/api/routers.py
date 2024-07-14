from fastapi.routing import APIRouter
from endpoints import auth, teacher, group, student, settings


api_routers = APIRouter()
api_routers.include_router(auth.auth_router, tags=["AUTH"])
api_routers.include_router(teacher.teacher_router, tags=["TEACHER"])
api_routers.include_router(group.group_router, tags=["GROUP"])
api_routers.include_router(student.student_router, tags=["STUDENT"])
api_routers.include_router(settings.setings_router, tags=["SETTINGS"])
