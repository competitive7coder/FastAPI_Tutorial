from fastapi import FastAPI
from src.books.routes import app as router

app = FastAPI(prefix="/books")

app.include_router(router)