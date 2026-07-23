from pydantic import BaseModel, EmailStr
from typing import List


class StudentCreate(BaseModel):
    name: str
    email: str


class StudentUpdate(BaseModel):
    name: str


class CourseCreate(BaseModel):
    title: str


class CourseResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    # student_id: int
    # course_id: int
    course: CourseResponse

    class Config:
        from_attributes = True


class StudentResponse(BaseModel):
    id: int
    name: str
    enrollments: List[EnrollmentResponse] = []

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DashboardResponse(BaseModel):
    total_student: int
    total_courses: int
    total_enrollments: int
    total_users: int
    popular_course: int
    students_without_courses: int
    course_without_student: int
    top_students: int
    popular_courses: int

class StudentPaginationResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int
    data: list[StudentResponse]

    class Config:
        from_attributes = True

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float

class AccountCreate(BaseModel):
    name: str
    balance: float

class AccountResponse(BaseModel):
    id: int
    name: str
    balance: float

    class Config:
        from_attributes = True