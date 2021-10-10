from fastapi import FastAPI, Depends, HTTPException, status, Response
import models.models as models
from typing import Optional, List
from sqlalchemy.orm import Session
from database.db import get_db
from routes import users, orders

app = FastAPI()

app.include_router(users.router)
app.include_router(orders.router)

@app.get('/')
async def index():
    return {"details": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)