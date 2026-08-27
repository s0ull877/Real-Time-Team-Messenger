from fastapi import Depends, FastAPI

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .infrastructure.config import get_settings
from .infrastructure.database import database as db


app_settings = get_settings()
app = FastAPI(
    title=app_settings.app_name,
    debug=app_settings.debug
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Real-Time Team Messenger"
    }


@app.get("/test")
async def root(session: AsyncSession = Depends(db.get_db_session)):

    print(app_settings.database_url)
    result = await session.execute(select(1))
    return {
        "status": "ok",
        "service": "Real-Time Team Messenger",
        "result": result.scalar()
    }