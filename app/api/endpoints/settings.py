from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

settings_router = APIRouter(prefix="/settings")


@settings_router.get(
    "/reset-db",
    status_code=status.HTTP_200_OK,
)
async def create_teacher():
    from app.database import engine
    from app.models import Base

    async with engine.begin() as connection:
        await connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        await connection.exec_driver_sql("CREATE SCHEMA public")
        await connection.run_sync(Base.metadata.create_all)
    return {"message": "Database schema was successfully reset."}


class LicenseRequest(BaseModel):
    kids: list
    type: str


@settings_router.post("/proxy/clearkey")
async def proxy_clearkey(request: LicenseRequest):
    url = "https://license.kinescope.io/v1/vod/fe1f558e-1043-4f47-9893-e6c924e40f79/acquire/clearkey?token="
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=request.dict(), headers=headers)
    return JSONResponse(content=response.json())
