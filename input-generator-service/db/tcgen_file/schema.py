from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TcGenFileCreate(BaseModel):
    tcgen_id: UUID
    filepath: str

class TcGenFileOut(BaseModel):
    tcgen_file_id: UUID
    tcgen_id: UUID
    filepath: str
    create_dt: datetime

    class Config:
        orm_mode = True