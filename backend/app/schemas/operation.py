from pydantic import BaseModel
from datetime import datetime

class OperationCreate(BaseModel):
    name: str
    description: str
    assembly_id: int

class OperationRead(OperationCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
