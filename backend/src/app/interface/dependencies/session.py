from typing import Annotated 
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import database, SQLAlchemyTransaction

SessionDep = Annotated[
    AsyncSession,
    Depends(database.get_db_session),
]