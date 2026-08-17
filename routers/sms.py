from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text  # type: ignore
from database import SessionLocal
from models import SmsBody
from schemas import SmsBodyBaseNotify
import logging
import pytz, requests
from dotenv import dotenv_values

env = dotenv_values(".env")


router = APIRouter(
    prefix="/sms",
    tags=["sms"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
logger = logging.getLogger("uvicorn.error")

@router.get("/test")
def get_sms(db: Session = Depends(get_db)):
    return {"message": "SMS router is working!"}


@router.post("/send-notify", status_code=status.HTTP_201_CREATED)
def add_sms_body(entry: SmsBodyBaseNotify, db: Session = Depends(get_db)):
    resp = requests.post('https://textbelt.com/text', {
        'phone': entry.number,
        'message': "Hi, that's Otis Harbor Springs and your table is ready. Please come to the host stand.",
        'key': env.get("SMS_TOKEN")
    })
    return resp.json()

@router.post("/quota", status_code=status.HTTP_200_OK)
def get_sms_quota():
    resp = requests.get(f'https://textbelt.com/quota/{env.get("SMS_TOKEN")}')
    return resp.json().get("quotaRemaining")

    