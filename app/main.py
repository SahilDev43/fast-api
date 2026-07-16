from fastapi import FastAPI
from app.database import Base, engine
from app.models import Student
from app.routers.students import router as student_router 
from app.routers import course
from app.routers import enrollments

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)

app.include_router(course.router)

app.include_router(enrollments.router)

