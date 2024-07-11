from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from config import config


def get_engine() -> AsyncEngine:
    url = config.DB_URL
    return create_async_engine(url=url, echo=False)

def get_asyncs_sessionmaker(engine: AsyncEngine) -> AsyncSession:
    return AsyncSession(
        bind=engine,
        expire_on_commit=False,
    )

engine = get_engine()
async_session = get_asyncs_sessionmaker(engine)