from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()

class Role(str, enum.Enum):
    admin = "admin"
    technologist = "technologist"
    assembler = "assembler"
    guest = "guest"

class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(Role), default=Role.guest, nullable=False)
