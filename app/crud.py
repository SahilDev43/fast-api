from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate
from app.models import Course
from app.models import Enrollment


def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_students(db: Session):
    return db.query(Student).all()

def get_students_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def update_student(db: Session, student_id: int, updated_student: StudentCreate):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        return None
    
    student.name = updated_student.name
    student.course = updated_student.course

    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        return None
    
    db.delete(student)
    db.commit()
    return student

def create_course(db: Session, course: Course):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_courses(db: Session):
    return db.query(Course).all()

def create_enrollment(
        db: Session,
        student_id: int,
        course_id: int
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        return "student_not_found", None
    
    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        return "course_not_found", None
    

    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        )
        .first()
    )

    if existing_enrollment:
        return "already_enrolled", None
    
    new_enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return "success", new_enrollment