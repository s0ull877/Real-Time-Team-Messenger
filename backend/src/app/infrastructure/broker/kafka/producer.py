import json
from dataclasses import asdict, is_dataclass
from typing import Any

from aiokafka import AIOKafkaProducer

from app.core.Ibroker import IBrokerProducer
from app.infrastructure.config import get_settings


settings = get_settings()


class KafkaProducer(IBrokerProducer):

    def __init__(self):
        self.producer: AIOKafkaProducer | None = None


    async def start(self):
        #! чтобы AIOKafkaProducer создавался не при импорте модуля, когда event loop FastAPI ещё не запущен.
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
        )
        
        try:
            await self.producer.start()
        except Exception:
            self.producer = None
            raise


    async def stop(self) -> None:

        if self.producer is not None:
            
            await self.producer.stop()
            self.producer = None


    async def publish(self, topic: str, message: Any) -> None:

        if is_dataclass(message):
            message = asdict(message)

        data = json.dumps(message).encode("utf-8")

        await self.producer.send_and_wait(topic, data)