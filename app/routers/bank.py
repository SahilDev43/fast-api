from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/bank",
    tags=["Bank"]
)

@router.post("/transfer")
def transfer_money(request: schemas.TransferRequest, db: Session = Depends(get_db)):
    return crud.transfer_money(db, request)