from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate
from app.models import Course
from app.models import Enrollment
from app.models import Account
from app import models, schemas, auth
from sqlalchemy import or_, func
from fastapi import HTTPException
import math


def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, search: str = "", sort: str = "name", page: int = 1, page_size: int = 10, name: str = "", email: str = ""):
    query = (
        db.query(models.Student)
        .filter(
            or_(
                models.Student.name.ilike(f"%{search}%"),
                models.Student.email.ilike(f"%{search}%")
            )
        )
    )

    filters = {
        "name": {
            "column": models.Student.name,
            "value": name,
            "operator": "ilike"
        },
        "email": {
            "column": models.Student.email,
            "value": email,
            "operator": "ilike"
        },
    }

    for key, filt in filters.items():
        if filt["value"]:
            if filt["operator"] == "ilike":
                query = query.filter(filt["column"].ilike(f"%{filt['value']}%"))

    descending = sort.startswith("-")
    sort = sort.lstrip("-")

    column = getattr(models.Student, sort, models.Student.name)

    if descending:
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column)

    total_records = query.count()

    total_pages = math.ceil(total_records / page_size)

    offset = (page - 1) * page_size
        
    students = (
    query
    .offset(offset)
    .limit(page_size)
    .all()
    )

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_records,
        "total_pages": total_pages,
        "data": students
    }


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


def get_student(db: Session, student_id: int):
    return (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )


def create_user(db, user: schemas.UserCreate):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        return None

    hashed_password = auth.hash_password(user.password)

    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authentication_user(db, email: str, password: str):
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if not user:
        return None

    if not auth.verify_password(password, user.hashed_password):
        return None

    return user


def get_student_courses(db: Session, course_id: int):
    students = (
        db.query(models.Student)
        .join(models.Enrollment)
        .filter(models.Enrollment.course_id == course_id)
        .all()
    )

    return students

def get_dashboard(db: Session):
    total_students = db.query(models.Student).count()
    total_courses = db.query(models.Course).count()
    total_enrollments = db.query(models.Enrollment).count()
    total_users = db.query(models.User).count()
    student_count = func.count(models.Enrollment.student_id)

    popular_course = (
    db.query(
        models.Course.title,
        student_count.label("student_count")
    )
    .outerjoin(models.Enrollment)
    .group_by(models.Course.id, models.Course.title)
    .order_by(student_count.desc())
    .first()
    )

    students_without_courses = (
        db.query(models.Student)
        .outerjoin(models.Enrollment, models.Enrollment.student_id == models.Student.id)
        .filter(models.Enrollment.id.is_(None))
        .count()        
    )

    course_without_student = (
        db.query(models.Course)
        .outerjoin(models.Enrollment, models.Enrollment.course_id == models.Course.id)
        .filter(models.Enrollment.id.is_(None))
        .count()
    )

    top_students = (
            db.query(
        models.Student.name.label("student_name"),
        func.count(models.Enrollment.id).label("total_courses")
    )

        .outerjoin(models.Enrollment, models.Enrollment.student_id == models.Student.id)
        .group_by(models.Student.id, models.Student.name)
        .order_by(func.count(models.Enrollment.id).desc())
        .limit(5)
        .all()
    )

    popular_courses = (
            db.query(
                models.Course.title.label("course_name"),
                student_count.label("student_count")
            )
            .join(
                models.Enrollment,
                models.Enrollment.course_id == models.Course.id
            )
            .group_by(
                models.Course.id,
                models.Course.title
            )
            .having(student_count > 2)
            .all()
        )

    return {
    "total_students": total_students,
    "total_courses": total_courses,
    "total_enrollments": total_enrollments,
    "total_users": total_users,

    "popular_course": (
        {
            "course_name": popular_course.title,
            "student_count": popular_course.student_count,
        }
        if popular_course
        else None
    ),

    "students_without_courses": students_without_courses,

    "courses_without_students": course_without_student,

    "top_students": [
        {
            "student_name": student.student_name,
            "total_courses": student.total_courses,
        }
        for student in top_students
    ],

    "popular_courses": [
        {
            "course_name": course.course_name,
            "student_count": course.student_count,
        }
        for course in popular_courses
    ],
}

def create_account(db: Session, account: Account):
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def transfer_money(db: Session, request: schemas.TransferRequest):
    try:
        sender = db.query(models.Account).filter(
            models.Account.id == request.from_account
        ).first()

        receiver = db.query(models.Account).filter(
            models.Account.id == request.to_account
        ).first()

        if not sender:
            raise HTTPException(status_code=404, detail="Sender account not found")

        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver account not found")

        if sender.balance < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        sender.balance -= request.amount
        receiver.balance += request.amount

        transaction = models.Transaction(
            from_account=request.from_account,
            to_account=request.to_account,
            amount=request.amount
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {"message": "Money transferred successfully"}

    except Exception:
        db.rollback()
        raise