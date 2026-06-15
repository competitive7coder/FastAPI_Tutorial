from fastapi import FastAPI, HTTPException,  Request
from schemas import Students, StudentResponse
from typing import List
from routes import router as student_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("Request started:", request.url)

    response = await call_next(request)

    print("Request finished")
    return response



app.include_router(student_router)