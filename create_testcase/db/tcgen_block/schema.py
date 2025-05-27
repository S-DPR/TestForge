from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Integer, Text
from psycopg2.extensions import JSONB


class TcGenBlockCreate(BaseModel):
    tcgen_id = UUID
    type = Text
    config = JSONB
    variable = JSONB
    output = JSONB
    repeat = Text
    sequence = Integer

class TcGenBlockOut(BaseModel):
    type = Text
    config = JSONB
    variable = JSONB
    output = JSONB
    repeat = Text
    sequence = Integer
    create_dt: datetime

    class Config:
        orm_mode = True