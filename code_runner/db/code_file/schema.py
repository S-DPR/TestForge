from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CodeFileCreate(BaseModel):
    account_id: UUID
    language: str
    filepath: str
    extension: str


class CodeFileOut(BaseModel):
    code_file_id: UUID
    filepath: str
    extension: str

    class Config:
        orm_mode = True