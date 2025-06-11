from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from user.routes.user import router as user_router

app = FastAPI()
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(user_router, prefix="/user")
app.include_router(v1_router)

origins = ["*"]

# Cors things.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}


# Mount frontend static files
frontend_path = Path(__file__).parent / "dist"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
