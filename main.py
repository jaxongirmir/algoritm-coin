from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
from app.api.routers import api_routers

app.include_router(api_routers)
from os import getenv

PGUSER = getenv("PGUSER")
PASSWORD = getenv("PGPASSWORD")
HOST = getenv("PGHOST")
PORT = getenv("PGPORT")
DATABASE = getenv("PGDATABASE")


print(f"postgresql+asyncpg://{PGUSER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
