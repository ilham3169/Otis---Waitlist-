from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Enum, DateTime, TIMESTAMP
from sqlalchemy.sql import func
from database import Base
import enum

class WaitlistStatus(str, enum.Enum):
    waiting = "waiting"
    notified = "notified"
    seated = "seated"
    no_show = "no_show"
    cancelled = "cancelled"

class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False, index=True)
    party_size = Column(Integer, nullable=False, default=1)
    status = Column(Enum(WaitlistStatus), nullable=False, default=WaitlistStatus.waiting, index=True)
    notes = Column(String(255), nullable=True)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notified_at = Column(DateTime, nullable=True)
    seated_at = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class SmsBody(Base):
    __tablename__ = "sms_bodies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String(255), nullable=False)
    number = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())