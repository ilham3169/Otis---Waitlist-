
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from models import WaitlistStatus

class WaitlistBase(BaseModel):
    name: str
    phone_number: str
    party_size: int = 1
    status: WaitlistStatus = WaitlistStatus.waiting
    notes: Optional[str] = None
    
class WaitlistCreate(WaitlistBase):
    pass

class WaitlistUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    party_size: Optional[int] = None
    status: Optional[Literal['waiting', 'notified', 'seated', 'no_show', 'cancelled']] = None
    notes: Optional[str] = None
    notified_at: Optional[datetime] = None
    seated_at: Optional[datetime] = None

class WaitlistOut(WaitlistBase):
    id: int
    joined_at: datetime
    notified_at: Optional[datetime] = None
    seated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SmsBodyBaseNotify(BaseModel):
    number: str


