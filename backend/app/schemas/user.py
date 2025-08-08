from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    technologist = "technologist"
    assembler = "assembler"
    guest = "guest"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role

class UserRead(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    role: Role

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[Role]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
