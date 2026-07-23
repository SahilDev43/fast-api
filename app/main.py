from fastapi import FastAPI
from app.database import Base, engine
from app.models import Student
from app.routers.students import router as student_router 
from app.routers import course
from app.routers import enrollments
from app.routers import users
from app.routers import dashboard
from app.routers import bank
from app.routers import account
from app.routers import files

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(student_router)

app.include_router(course.router)

app.include_router(enrollments.router)

app.include_router(users.router)

app.include_router(dashboard.router)

app.include_router(bank.router)

app.include_router(account.router)

app.include_router(files.router)