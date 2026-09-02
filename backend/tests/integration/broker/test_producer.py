import json
from uuid import uuid4

import pytest
from aiokafka import AIOKafkaConsumer

from app.infrastructure.broker.kafka.producer import KafkaProducer
from app.infrastructure.config import get_settings


settings = get_settings()


@pytest.mark.asyncio
async def test_publish():
    
    topic = f"test-topic-{uuid4()}"
    message = {
        "email": "test@example.com",
        "subject": "Test message",
        "body": "Hello from integration test",
    }

    producer = KafkaProducer()

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=f"test-group-{uuid4()}",
        auto_offset_reset="earliest",
    )

    await producer.start()
    await consumer.start()

    try:
        await producer.publish(
            topic=topic,
            message=message,
        )

        result = await consumer.getone()

        received_message = json.loads(result.value.decode("utf-8"))

        assert received_message == message

    finally:
        await consumer.stop()
        await producer.stop()