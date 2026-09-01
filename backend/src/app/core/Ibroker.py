from abc import ABC, abstractmethod
from .entities import EmailMessage


class IBrokerProducer(ABC):

    @abstractmethod
    async def publish_email(self, email_message: EmailMessage) -> None:

        raise NotImplementedError