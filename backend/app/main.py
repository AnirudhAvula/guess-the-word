from fastapi import FastAPI

from app.database import client
from app.routes.auth import router as auth_router
from app.routes.game import router as game_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.admin import router as admin_router

app = FastAPI(
    title="Guess the Word API",
    description="Backend API for the Guess the Word game",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(game_router)
app.include_router(admin_router)

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