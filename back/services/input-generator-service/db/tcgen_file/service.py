from sqlalchemy.orm import Session
from uuid import UUID
from db.tcgen_file.model import TcGenFile
from db.tcgen_file.schema import TcGenFileCreate
from datetime import datetime

def create_tcgen_file(db: Session, data: TcGenFileCreate):
    obj = TcGenFile(
        tcgen_id=data.tcgen_id,
        filepath=data.filepath,
        create_dt=datetime.utcnow()
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_tcgen_file(db: Session, file_id: UUID):
    return db.get(TcGenFile, file_id)

def get_all_tcgen_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TcGenFile).offset(skip).limit(limit).all()

def delete_tcgen_file(db: Session, file_id: UUID):
    obj = db.get(TcGenFile, file_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
