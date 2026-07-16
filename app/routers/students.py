from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import StudentCreate
from app.models import Student
from fastapi import HTTPException
import app.crud as crud

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    new_student = Student(
        name=student.name,
        course=student.course
    )

    return crud.create_student(db, new_student)


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@router.get("/{student_id}")
def get_students_id(student_id: int, db: Session = Depends(get_db)):
    get_id = crud.get_students_id(db, student_id)

    if get_id is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return get_id


@router.put("/{student_id}")
def update_student(student_id: int, updated_student: StudentCreate, db: Session = Depends(get_db)):
    student = crud.update_student(db, student_id, updated_student)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student_id)
    if delete_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return delete_student