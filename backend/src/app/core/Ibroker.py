from abc import ABC, abstractmethod
from typing import Any


class IBrokerProducer(ABC):

    @abstractmethod
    async def publish(self, topic: str, message: Any) -> None:
        raise NotImplementedError