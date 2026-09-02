import asyncio
from fastapi import Depends, FastAPI

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from .infrastructure.config import get_settings
from .infrastructure.database import database as db
from .infrastructure.broker.kafka import KafkaProducer
from .infrastructure.broker.kafka import EmailConsumer
from .infrastructure.SMTPclient import SMTPClient

app_settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):

    kafka_producer = KafkaProducer()
    kafka_email_consumer = EmailConsumer(mailer=SMTPClient)

    await kafka_producer.start()
    await kafka_email_consumer.start()

    consumer_task = asyncio.create_task(
        kafka_email_consumer.consume()
    )

    try:
        yield
    finally:

        consumer_task.cancel()

        try:
            await consumer_task
        except asyncio.CancelledError:
            pass

        await kafka_email_consumer.stop()
        await kafka_producer.stop()


app = FastAPI(
    lifespan=lifespan,
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