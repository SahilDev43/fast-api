from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CourseCreate
from app.models import Course
import app.crud as crud

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = Course(
        title=course.title
    )
    return crud.create_course(db, new_course)

@router.get("/")
def get_courses(
    db: Session = Depends(get_db)
):
    return crud.get_courses(db)