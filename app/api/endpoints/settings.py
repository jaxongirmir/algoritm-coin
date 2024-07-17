from fastapi import APIRouter, status

settings_router = APIRouter(prefix="/settings")


@settings_router.get(
    "/reset-db",
    status_code=status.HTTP_200_OK,
)
async def reset_database():
    from ...database import engine
    from ...models import Base

    async with engine.begin() as connection:
        await connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        await connection.exec_driver_sql("CREATE SCHEMA public")
        await connection.run_sync(Base.metadata.create_all)
    return {"message": "Database schema was successfully reset."}
