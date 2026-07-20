from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.schemas import StudentCreate, StudentResponse
from app.models import Student
from app.models import Enrollment
from fastapi import HTTPException
import app.crud as crud
from app import oauth2
from app import schemas
from app.schemas import StudentResponse

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
        name=student.name
    )

    return crud.create_student(db, new_student)


@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return crud.get_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
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
    return deleted_student

@router.get("/test/lazy")
def test_lazy(db: Session = Depends(get_db)):
    student = (db.query(Student).options(
        joinedload(Student.enrollments)
        .joinedload(Enrollment.course)
    )
    .first()
    )

    for enrollment in student.enrollments:
        print(enrollment.course.title)

    return {
         "message": "Done"
    }