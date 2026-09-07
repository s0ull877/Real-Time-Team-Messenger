from uuid import UUID
from dataclasses import dataclass

from app.core.entities import EmailMessage
from app.core.Ibroker import IBrokerProducer

from app.infrastructure.config import get_settings


settings = get_settings()

@dataclass
class MailService:
    
    def __init__(
        self,
        broker_producer: IBrokerProducer,
    ):
        
        self.broker_producer = broker_producer


    async def send_verify_token(self, to: str, token: str) -> None:
        
        # Create verification email.

        email_message = EmailMessage(
            email=to, 
            subject=f"Verification link for {to}", 
            body=f"Go to {settings.server_url}auth/verify-email/{token} for verifying your account"
        )


        await self.broker_producer.publish(topic="emails",message=email_message)

        return


    async def send_reset_password_token(self, to: str, token: str) -> None:
        
        # Create reset password token email.

        email_message = EmailMessage(
            email=to, 
            subject=f"Verification link for {to}", 
            body=f"Go to {settings.server_url}auth/reset-password/{token} for reset your password"
        )


        await self.broker_producer.publish(topic="emails",message=email_message)

        return


    async def send_change_email_token(self, to: str, token: str) -> None:
        
        # Create reset password token email.

        email_message = EmailMessage(
            email=to, 
            subject=f"Verification link for {to}", 
            body=f"Go to {settings.server_url}auth/change-email/{token} for change your email"
        )


        await self.broker_producer.publish(topic="emails",message=email_message)

        return


    async def send_room_invitation_token(self, to: str, token: str, sender_username: str, room_id: UUID, room_name: str) -> None:
        
        # Create reset password token email.

        email_message = EmailMessage(
            email=to, 
            subject=f"@{sender_username} invite you to your room '{room_name}'", 
            body=f"Go to {settings.server_url}rooms/{room_id}/accept/{token} for accept an invitation and join!"
        )


        await self.broker_producer.publish(topic="emails",message=email_message)

        return