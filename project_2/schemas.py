from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    department: str

    class Config:
        from_attributes = True  # IMPORTANT (SQLAlchemy → Pydantic)
