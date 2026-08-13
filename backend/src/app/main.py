import uvicorn
from .infrastructure.config import get_settings

settings = get_settings()

def main():
    uvicorn.run(
        "app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )