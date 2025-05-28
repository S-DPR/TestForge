from uuid import UUID
from sqlalchemy.orm import Session

from db.code_run.model import CodeRun
from db.code_run import schema


def create_code_run(db: Session, data: schema.CodeRunCreate):
    code_run = CodeRun(
        account_id=data.account_id,
        language=data.language,
    )
    db.add(code_run)
    db.commit()
    db.refresh(code_run)
    return code_run


def get_all_code_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CodeRun).offset(skip).limit(limit).all()


def get_code_run(db: Session, code_run_id: UUID):
    return db.query(CodeRun).filter(CodeRun.code_run_id == code_run_id).first()


def delete_code_run(db: Session, code_run_id: UUID):
    obj = db.query(CodeRun).filter(CodeRun.code_run_id == code_run_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
