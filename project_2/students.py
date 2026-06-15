from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()


@router.post("/students", response_model=schemas.StudentResponse, status_code=201)
def add_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    # check duplicate
    existing_student = db.query(models.Student).filter(
        models.Student.name == student.name,
        models.Student.department == student.department
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    new_student = models.Student(
        name=student.name,
        department=student.department
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student



@router.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()




@router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.department = student.department

    db.commit()
    db.refresh(db_student)

    return db_student



@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()





















# from fastapi import APIRouter, HTTPException
# from models import Student

# router = APIRouter()

# students: list[Student] = []

# @router.get("/students")
# def get_students_details():
#     return students

# @router.post("/students", status_code=201)
# def add_student(student: Student):
#     for s in students:
#         if s.name == student.name and s.department == student.department:
#             raise HTTPException(status_code=400, detail="Student already exists")
#     students.append(student)
#     return student

# @router.put("/students/{student_id}")
# def update_student(student_id: int, student: Student):
#     for i in range(len(students)):
#         if students[i].id == student_id:
#             student.id = student_id
#             students[i] = student
#             return student
#     raise HTTPException(status_code=404, detail="Student not found")

# @router.delete("/students/{student_id}", status_code=204)
# def delete_student(student_id: int):
#     for i, s in enumerate(students):
#         if s.id == student_id:
#             students.pop(i)
#             return
#     raise HTTPException(status_code=404, detail="Student not found")
