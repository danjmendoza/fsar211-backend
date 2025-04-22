from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from sqlalchemy.orm import Session
import Schema
from models.user import User
from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    return {"Hello": "Welcome to the 211"}

@app.get("/user", response_model=List[Schema.CreateUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=List[Schema.CreateUser])
def post_user(user:Schema.CreateUser, db:Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return [new_user]



@app.get("/time_log", tags=['time_log'])
async def get_time_log() -> dict:
    return { "data": time_logs}

@app.post("/time_log", tags=["time_log"])
async def add_time_log(time_log: dict) -> dict:
    time_logs.append(time_log)
    return {
        "data": { "Time log added."}
    }

@app.get("/user/{id}", tags=['users'])
async def get_user(id: int) -> dict:
    if id not in users:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {
        "data": users[id]
    }