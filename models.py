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
    joined_at = Column(DateTime, server_default=func.now())
    notified_at = Column(DateTime, nullable=True)
    seated_at = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# # models.py
# from database import Base
# from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, Boolean, Date, ForeignKey
# from sqlalchemy.sql import func

# class User(Base):
#     __tablename__ = "users"

#     user_id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     password = Column(String(50), nullable=False)
#     email = Column(String(100), nullable=True, unique=True)
#     phone_number = Column(String(15), nullable=True)
#     membership_id = Column(String(50), ForeignKey("memberships.membership_id"), nullable=True, unique=True)
#     status = Column(Enum('active', 'inactive', 'suspended'), default='active')
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
#     entry_count = Column(Integer, default=0)
#     last_entry = Column(TIMESTAMP, nullable=True)
#     is_admin = Column(Boolean, default=False)
#     is_inside = Column(Boolean, default=False)

# class Membership(Base):
#     __tablename__ = "memberships"

#     membership_id = Column(String(50), primary_key=True)
#     membership_type = Column(String(50), nullable=False)
#     is_active = Column(Boolean, default=True)
#     entry_limit = Column(Integer, nullable=False)
#     price = Column(Integer, nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


# class RFIDCard(Base):
#     __tablename__ = "rfid_cards"

#     card_id = Column(String(100), primary_key=True)  # Use RFID UID as primary key
#     user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     last_used_at = Column(TIMESTAMP, nullable=True)
