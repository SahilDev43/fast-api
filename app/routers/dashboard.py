from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
import app.crud as crud

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard(db)