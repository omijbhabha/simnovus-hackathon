from fastapi import FastAPI

app = FastAPI(
    title="Simnovus Device Fleet Monitor",
    description="A simple API for monitoring device heartbeats and fleet status.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Simnovus Device Fleet Monitor is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}