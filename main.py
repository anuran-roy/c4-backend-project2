from fastapi import FastAPI
from routes import users, orders, restaurants, cities, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(restaurants.router)
app.include_router(cities.router)


@app.get('/', tags=["CheckServerStatus"])
async def index():
    return {"details": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)
