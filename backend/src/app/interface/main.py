import asyncio
from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.infrastructure.config import get_settings
from app.infrastructure.broker.kafka import KafkaProducer
from app.infrastructure.broker.kafka import EmailConsumer
from app.infrastructure.SMTPclient import SMTPClient

from app.core.exceptions import AppError

from .handlers import app_error_handler
from .routers import router

app_settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):

    producer = KafkaProducer()
    app.state.producer = producer #для передачи в dependency

    email_consumer = EmailConsumer(
        mailer=SMTPClient,
    )

    await producer.start()
    await email_consumer.start()

    consumer_task = asyncio.create_task(
        email_consumer.consume()
    )

    try:
        yield

    finally:
        consumer_task.cancel()

        try:
            await consumer_task
        except asyncio.CancelledError:
            pass

        await email_consumer.stop()
        await producer.stop()


app = FastAPI(
    lifespan=lifespan,
    title=app_settings.app_name,
    debug=app_settings.debug,
)


app.add_exception_handler(
    AppError,
    app_error_handler,
)

app.include_router(router=router, prefix="/api")