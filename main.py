from fastapi import FastAPI, Depends, HTTPException, status, Response
import models.models as m
import modules.hashing as h
from typing import  Optional, List
from sqlalchemy.orm import  Session
# from database.db import engine, SessionLocal

app = FastAPI()

@app.get('/')
async def index():
    return {"details": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)