from fastapi import HTTPException, APIRouter, Depends, status
from typing import Annotated, List
from schemas import Students, StudentResponse,LATERAL_STUDENT

router = APIRouter(prefix="/students", tags=["Students"])


fake_db: List[Students] = []



def get_fake_db() -> List[Students]:
    return fake_db

DB = Annotated[List[Students], Depends(get_fake_db)]

# -------------------- CREATE --------------------

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: Students,
    db: DB
):
    if any(s.id == student.id for s in db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already exists"
        )

    db.append(student)
    return student


DynamicStudent = LATERAL_STUDENT
@router.post("/lateral", response_model=DynamicStudent)
def create_lateral_student(
    student: DynamicStudent,
    db: DB
):
    if any(s.id == student.id for s in db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already exists"
        )

    db.append(student)
    return student


# -------------------- READ ALL --------------------

@router.get("/", response_model=List[StudentResponse])
def get_students(db: DB):
    return db

# -------------------- READ ONE --------------------

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: DB):
    student = next((s for s in db if s.id == student_id), None)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student

# -------------------- UPDATE --------------------

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_student: Students,
    db: DB
):
    for index, student in enumerate(db):
        if student.id == student_id:
            updated_student.id = student_id  # keep path id authoritative
            db[index] = updated_student
            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

# -------------------- DELETE --------------------

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: DB):
    for index, student in enumerate(db):
        if student.id == student_id:
            db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )