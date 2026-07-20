from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import oauth2

from app.database import get_db
from app import crud, schemas
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authentication_user(
        db,
        user_credentials.username,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }