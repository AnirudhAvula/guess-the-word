from fastapi import FastAPI

from app.database import client


app = FastAPI(
    title="Guess the Word API",
    description="Backend API for the Guess the Word game",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Guess the Word API is running"
    }


@app.get("/health")
def health_check():
    try:
        client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }