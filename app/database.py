from os import getenv
from dotenv_vault import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

load_dotenv(".env")

USER = getenv("PGUSER")
PASSWORD = getenv("PGPASSWORD")
HOST = getenv("PGHOST")
PORT = getenv("PGPORT")
DATABASE = getenv("PGDATABASE")

engine = create_async_engine(
    url=make_url(
        name_or_url=f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    ),
    echo=True,
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
