from fastapi import FastAPI
from .infrastructure.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Real-Time Team Messenger"
    }