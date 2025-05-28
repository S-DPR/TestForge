from uuid import UUID
from sqlalchemy.orm import Session
from db.code_res.model import CodeRes
from db.code_res import schema


def create_code_res(db: Session, data: schema.CodeResCreate):
    code_res = CodeRes(
        code_file_id=data.code_file_id,
        input_filepath=data.input_filepath,
        exitcode=data.exitcode,
        # execute_time=data.execute_time,
        # memory=data.memory,
        output_filepath=data.output_filepath,
    )
    db.add(code_res)
    db.commit()
    db.refresh(code_res)
    return code_res


def get_all_code_res(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CodeRes).offset(skip).limit(limit).all()


def get_code_res(db: Session, code_res_id: UUID):
    return db.query(CodeRes).filter(CodeRes.code_res_id == code_res_id).first()


def delete_code_res(db: Session, code_res_id: UUID):
    obj = db.query(CodeRes).filter(CodeRes.code_res_id == code_res_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
