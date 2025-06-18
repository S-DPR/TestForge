from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CodeResCreate(BaseModel):
    code_file_id: UUID
    input_filepath: str
    exitcode: int
    # execute_time: int
    # memory: int
    output_filepath: str


class CodeResOut(BaseModel):
    code_res_id: UUID
    input_filepath: str
    exitcode: int
    # execute_time: int
    # memory: int
    output_filepath: str
    create_dt: datetime

    class Config:
        orm_mode = True