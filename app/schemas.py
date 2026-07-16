from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    course: str

class StudentUpdate(BaseModel):
    name: str
    course: str

class StudentResponse(BaseModel):
    id: int
    name: str
    course: str

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str


class CourseResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attribute = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attribute = True