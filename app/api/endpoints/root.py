from fastapi import APIRouter
from fastapi.responses import RedirectResponse


root_router = APIRouter()


@root_router.get("/")
async def root():
    return RedirectResponse(url="/docs")
