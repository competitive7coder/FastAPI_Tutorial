from fastapi import FastAPI
from auth import router as auth_router
from students import router as student_router
from file import router as file_router
from database import engine
from models import Base

app = FastAPI()

app.include_router(auth_router)
app.include_router(student_router)
app.include_router(file_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return {"MESSAGE": "HELLO! PROTYUSH"}
