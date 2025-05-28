from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Integer, Text


class TcGenBlockCreate(BaseModel):
    tcgen_id: UUID
    type: Text
    config: dict
    variable: dict
    output: dict
    repeat: Text
    sequence: Integer

class TcGenBlockOut(BaseModel):
    type: Text
    config: dict
    variable: dict
    output: dict
    repeat: Text
    sequence: Integer
    create_dt: datetime

    class Config:
        orm_mode = True