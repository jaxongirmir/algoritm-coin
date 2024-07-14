from fastapi import APIRouter, status

setings_router = APIRouter(prefix="/settings")


@setings_router.get(
    "/reset-db",
    status_code=status.HTTP_200_OK,
)
async def create_teacher():
    from app.database import engine
    from app.models import Base, Teacher, Group, Student

    async with engine.begin() as connection:
        await connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        await connection.exec_driver_sql("CREATE SCHEMA public")
        await connection.run_sync(Base.metadata.create_all)
