from fastapi import FastAPI
from src.books.routes import app as router

app = FastAPI(prefix = "/books", tags = ["Books"])
app.include_router(router)
