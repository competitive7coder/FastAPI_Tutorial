from pydantic import BaseModel, Field, StringConstraints, create_model
from typing import Annotated

class Students(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=4, max_length=10)]
    department: Annotated[str, Field(min_length=2, max_length=40)] 
    # department: str = Field(..., min_length=2, max_length=40)
    year: Annotated[int, Field(ge=1900, le=2026)]

class StudentResponse(BaseModel):
    name: str
    department: str

LATERAL_STUDENT = create_model(
    "LateralStudent",
    id=(int, Field(..., gt=0)),
    name=(str, Field(..., min_length=2, max_length=20)),
    # name=(Annotated[str, Field(min_length=4, max_length=10)], ...), ****DONT USE ANNOTATED IN CREATE_MODEL****
    department=(str, Field(..., min_length=2, max_length=40)),
    year=(int, Field(..., ge=1900, le=2026))
)

# *****ALREADY HAS STUDENT_RESPONSE FIELDS, SO NO NEED TO CREATE A NEW MODEL*****

# LATERAL_STUDENT_RESPONSE = create_model(
#     "LateralStudentResponse",
#     name=(str, Field(..., min_length=4, max_length=10)),    
#     department=(str, Field(..., min_length=2, max_length=40))
# )