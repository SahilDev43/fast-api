from pydantic import BaseModel
from typing import List


class StudentCreate(BaseModel):
    name: str


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
