from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TcGenCreate(BaseModel):
    account_id: UUID

class TCGenOut(BaseModel):
    tcgen_id: UUID
    account_id: UUID
    create_dt: datetime

    class Config:
        orm_mode = True