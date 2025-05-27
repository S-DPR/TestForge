from uuid import UUID

from sqlalchemy.orm import Session

from db.tcgen.model import TcGen
from db.tcgen import schema

def create_tcgen(db: Session, data: schema.TcGenCreate):
    tcgen = TcGen(
        account_id=data.account_id,
    )
    db.add(tcgen)
    db.commit()
    db.refresh(tcgen)
    return tcgen

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TcGen).offset(skip).limit(limit).all()

def get_tcgen(db: Session, tcgen_id: UUID):
    return db.query(TcGen).filter(TcGen.tcgen_id == tcgen_id).first()

def delete_tcgen(db: Session, tcgen_id: UUID):
    obj = db.query(TcGen).get(tcgen_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
