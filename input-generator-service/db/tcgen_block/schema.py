from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Integer, Text


class TcGenBlockCreate(BaseModel):
    tcgen_id: UUID
    type: str
    config: dict
    variable: list
    output: dict
    repeat: str
    sequence: int

class TcGenBlockOut(BaseModel):
    type: str
    config: dict
    variable: list
    output: dict
    repeat: str
    sequence: int
    create_dt: datetime

    class Config:
        orm_mode = True