from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Real-Time Team Messenger"
    }