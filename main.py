from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_routers

app = FastAPI(
    title="Algoritm Coins",
    description='API-documentation for "Algoritm" coin system',
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routers)
app.mount("/static", StaticFiles(directory="static"), name="static")
