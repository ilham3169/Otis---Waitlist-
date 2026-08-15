from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text  # type: ignore
from database import SessionLocal
from models import WaitlistEntry
from schemas import WaitlistOut, WaitlistCreate, WaitlistUpdate
import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError  # type: ignore
import pytz

TIMEZONE = pytz.timezone("Asia/Baku")

router = APIRouter(
    prefix="/waitlist",
    tags=["waitlist"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
logger = logging.getLogger("uvicorn.error")


@router.get("", response_model=List[WaitlistOut])
def get_waitlist_entries(db: Session = Depends(get_db)):
    entries = db.query(WaitlistEntry).all()
    return entries