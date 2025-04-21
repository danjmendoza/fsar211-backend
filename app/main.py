from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


users = {
    531: {
        "id": 531,
        "name": "Dan Mendoza",
        "resource_type": "Fremont Search And Rescue"
    }
}

time_logs = [
    {
        "id": 531,
        "name": "Dan Mendoza",
        "resource_type": "FSAR",
        "date_in": "June 3rd 2025",
        "time_in": "0800",
        "date_out": "June 3rd 2025",
        "time_out": "1000"
    }
]

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