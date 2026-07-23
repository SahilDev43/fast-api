from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AccountCreate
from app.models import Account
import app.crud as crud

router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@router.post("/")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):

    new_account = Account(
        name=account.name,
        balance=account.balance
    )
    return crud.create_account(db, new_account)