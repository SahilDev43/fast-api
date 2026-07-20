from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserResponse)
def register_user(user: schemas. UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    if new_user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return new_user