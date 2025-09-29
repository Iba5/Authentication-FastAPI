from fastapi import FastAPI
from .database.config import create_db,engine
from contextlib import asynccontextmanager
from .controller.endpoints import router as paths

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Starting Db")
    #logic for the db
    create_db()
    yield
    #close db as soon as the app stop
    engine.dispose()
    print("db closed")

app=FastAPI(lifespan=life_span, title="Authenticator",description="Here we are going to filter all the user")
app.include_router(paths)