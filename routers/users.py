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


@router.get("/all-users", response_model=List[WaitlistOut])
def get_waitlist_entries(db: Session = Depends(get_db)):
    entries = db.query(WaitlistEntry).all()
    return entries

@router.post("/create", response_model=WaitlistOut, status_code=status.HTTP_201_CREATED)
def add_waitlist_entry(entry: WaitlistCreate, db: Session = Depends(get_db)):
    new_entry = WaitlistEntry(          
        name=entry.name,
        phone_number=entry.phone_number,
        party_size=entry.party_size,
        status=entry.status,
        notes=entry.notes,
    )
    db.add(new_entry)                   
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.delete("/{entry_id}", status_code=status.HTTP_200_OK)
def delete_waitlist_entry(entry_id: int, db: db_dependency):
    entry = db.query(WaitlistEntry).filter(WaitlistEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db.delete(entry)
    db.commit()

    return {"message": "Entry deleted successfully", "deleted_id": entry_id}

@router.patch("/edit/{entry_id}", status_code=status.HTTP_200_OK)
def update_waitlist_entry(entry_id: int, payload: WaitlistUpdate, db: db_dependency):
    entry = db.query(WaitlistEntry).filter(WaitlistEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)

    return {
        "message": "Entry updated successfully",
        "entry": {
            "id": entry.id,
            "name": entry.name,
            "phone_number": entry.phone_number,
            "party_size": entry.party_size,
            "status": entry.status,
            "notes": entry.notes
        },
    }