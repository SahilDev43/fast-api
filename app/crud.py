from sqlalchemy.orm import Session
from app.models import Student


def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_students(db: Session):
    return db.query(Student).all()

def get_students_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()