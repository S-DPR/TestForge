from uuid import UUID

from sqlalchemy.orm import Session

from create_testcase.db.tcgen_block.model import TcGenBlock
from create_testcase.db.tcgen_block import schema

def create_tcgen_block(db: Session, data: schema.TcGenBlockCreate):
    tcgen_block = TcGenBlock(
        tcgen_id = data.tcgen_id,
        type = data.type,
        config = data.config,
        variable = data.variable,
        output = data.output,
        repeat = data.repeat,
        sequence = data.sequence,
    )
    db.add(tcgen_block)
    db.commit()
    db.refresh(tcgen_block)
    return tcgen_block

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TcGenBlock).offset(skip).limit(limit).all()

def get_tcgen_block(db: Session, tcgen_block_id: UUID):
    return db.query(TcGenBlock).filter(TcGenBlock.tcgen_block_id == tcgen_block_id).first()

def delete_tcgen_block(db: Session, tcgen_block_id: UUID):
    obj = db.query(TcGenBlock).get(tcgen_block_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
