import uuid
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.preset.model import Preset
from db.preset import schema

from error.exception import PresetNotFoundError

def create_preset(db: Session, data: schema.PresetCreate):
    preset = Preset(
        preset_name=data.preset_name,
        preset_type=data.preset_type,
        content=data.content,
        account_id=data.account_id
    )
    db.add(preset)
    db.commit()
    db.refresh(preset)
    return preset

def update_preset(db: Session, data: schema.PresetUpdate):
    preset = db.query(Preset).filter(Preset.preset_id == data.preset_id).first()
    if not preset:
        raise PresetNotFoundError("Preset not found")

    preset.preset_name = data.preset_name
    preset.preset_type = data.preset_type
    preset.content = data.content
    preset.account_id = data.account_id

    db.commit()
    db.refresh(preset)
    return preset

def get_all_presets(db: Session, account_id: UUID, page: int = 0, size: int = 100):
    offset = page * size
    return (
        db.query(Preset)
        .filter(
            or_(
                Preset.visibility == 'PUBLIC',
                Preset.account_id == account_id
            )
        )
        .offset(offset)
        .limit(size)
        .all()
    )

def get_preset(db: Session, preset_id: UUID):
    return db.query(Preset).filter(Preset.preset_id == preset_id).first()

def delete_preset(db: Session, preset_id: UUID):
    obj = db.query(Preset).get(preset_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False