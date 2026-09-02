import asyncio
import json
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from aiokafka import AIOKafkaProducer

from app.core.entities import EmailMessage
from app.infrastructure.broker.kafka.consumers.email_consumer import EmailConsumer
from app.infrastructure.config import get_settings


settings = get_settings()


class FakeEmailMailer:

    def __init__(self) -> None:
        self.messages: list[EmailMessage] = []

    async def send_email(self, message: EmailMessage) -> None:
        self.messages.append(message)


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
async def email_consumer() -> AsyncGenerator[tuple[EmailConsumer, FakeEmailMailer], None]:
    
    mailer = FakeEmailMailer()

    consumer = EmailConsumer(mailer=mailer, auto_offset_reset="latest")
    consumer.group_id = f"email-consumer-test-{uuid.uuid4()}"

    await consumer.start()

    try:
        yield consumer, mailer
    finally:
        await consumer.stop()


@pytest.mark.asyncio
async def test_email_consumer_receives_message(kafka_producer: AIOKafkaProducer, 
                            email_consumer: tuple[EmailConsumer, FakeEmailMailer]) -> None:
    
    consumer, mailer = email_consumer
    consume_task = asyncio.create_task(consumer.consume())
    await asyncio.sleep(0.2)

    message = EmailMessage(
        email="test@example.com",
        subject="Test subject",
        body="Test body",
    )

    await kafka_producer.send_and_wait(
        consumer.topic,
        json.dumps(
            {
                "email": message.email,
                "subject": message.subject,
                "body": message.body,
            }
        ).encode("utf-8"),
    )


    for _ in range(50):

        if mailer.messages:

            break

        await asyncio.sleep(0.1)

    consume_task.cancel()

    with pytest.raises(asyncio.CancelledError):
        
        await consume_task

    assert mailer.messages == [message]