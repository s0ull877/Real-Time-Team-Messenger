import asyncio
import json
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from aiokafka import AIOKafkaProducer

from app.core.entities import EmailMessage
from app.infrastructure.SMTPclient import AsyncSMTPMailer
from app.infrastructure.broker.kafka.consumers.email_consumer import EmailConsumer
from app.infrastructure.config import get_settings


settings = get_settings()


@pytest_asyncio.fixture
async def kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
    )

    await producer.start()

    try:
        yield producer
    finally:
        await producer.stop()


@pytest_asyncio.fixture
async def email_consumer() -> AsyncGenerator[EmailConsumer, None]:
    mailer = AsyncSMTPMailer()

    consumer = EmailConsumer(
        mailer=mailer,
        auto_offset_reset="latest",
    )

    consumer.group_id = f"email-consumer-test-{uuid.uuid4()}"

    await consumer.start()

    try:
        yield consumer
    finally:
        await consumer.stop()


@pytest.mark.asyncio
async def test_email_full_cycle(
    kafka_producer: AIOKafkaProducer,
    email_consumer: EmailConsumer,
) -> None:
    consumer_task = asyncio.create_task(
        email_consumer.consume()
    )

    await asyncio.sleep(0.5)

    message = EmailMessage(
        email="write.your.email@test.com",
        subject="Real-Time Team Messenger integration test",
        body="Kafka -> EmailConsumer -> SMTP",
    )

    await kafka_producer.send_and_wait(
        email_consumer.topic,
        json.dumps(
            {
                "email": message.email,
                "subject": message.subject,
                "body": message.body,
            }
        ).encode("utf-8"),
    )

    await asyncio.sleep(2)

    consumer_task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await consumer_task