from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EnrollmentCreate, EnrollmentResponse
import app.crud as crud

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    status, data = crud.create_enrollment(
        db,
        enrollment.student_id,
        enrollment.course_id
    )

    if status == "student_not_found":
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if status == "course_not_found":
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    
    if status == "already_enrolled":
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this course"
        )

    return data

@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student