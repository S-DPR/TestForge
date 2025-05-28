from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CodeRunCreate(BaseModel):
    account_id: UUID
    language: str


class CodeRunOut(BaseModel):
    code_run_id: UUID
    account_id: UUID
    language: str
    create_dt: datetime

    class Config:
        orm_mode = True
