import uvicorn
from .infrastructure.config import get_settings

app_settings = get_settings()

def main():
    uvicorn.run(
        "app:app",
        host=app_settings.app_host,
        port=app_settings.app_port,
        reload=True,
    )