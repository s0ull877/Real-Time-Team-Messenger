import json

from aiokafka import AIOKafkaConsumer

from app.core.entities import EmailMessage
from app.infrastructure.config import get_settings
from app.infrastructure.SMTPclient import AsyncSMTPMailer


settings = get_settings()


class EmailConsumer:

    topic = "emails"
    group_id = "email-consumer"


    def __init__(self, mailer: AsyncSMTPMailer, auto_offset_reset: str = "earliest") -> None:

        self.mailer = mailer
        self.auto_offset_reset = auto_offset_reset
        self.consumer: AIOKafkaConsumer | None = None


    async def start(self) -> None:

        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=self.auto_offset_reset
        )

        try:

            await self.consumer.start()

        except Exception:

            self.consumer = None
            raise


    async def stop(self) -> None:

        if self.consumer is not None:

            await self.consumer.stop()
            self.consumer = None


    async def consume(self) -> None:

        if self.consumer is None:

            raise RuntimeError("Email consumer is not started")

        async for message in self.consumer:

            data = json.loads(message.value.decode("utf-8"))
            email_message = EmailMessage(**data)
            await self.handle_message(email_message)


    async def handle_message(self, message: EmailMessage) -> None:

        await self.mailer.send_email(message)