from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from user.routes.user import router as user_router
from db import Base, engine

app = FastAPI()
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(user_router, prefix="/user")
app.include_router(v1_router)

origins = [
    "https://localhost:5173",
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {
        "Hello": "Welcome to the 211 some chagne in the code",
        "and": "then some masdfcore change",
        "or": "then some more change"
    }