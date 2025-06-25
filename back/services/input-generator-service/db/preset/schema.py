from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr


class PresetCreate(BaseModel):
    preset_name: constr(min_length=1, max_length=20)
    preset_type: constr(min_length=1)
    content: constr(min_length=1)
    account_id: Optional[UUID] = None

class PresetUpdate(BaseModel):
    preset_id: UUID
    preset_name: constr(min_length=1, max_length=20)
    preset_type: constr(min_length=1)
    content: constr(min_length=1)
    account_id: Optional[UUID] = None

class PresetOut(BaseModel):
    preset_id: UUID
    preset_name: str
    preset_type: str
    content: str
    account_id: Optional[UUID]
    create_dt: datetime
    update_dt: datetime

    class Config:
        orm_mode = True