from uuid import UUID
from sqlalchemy.orm import Session
from create_testcase.db.code_file.model import CodeFile
from create_testcase.db.code_file import schema


def create_code_file(db: Session, data: schema.CodeFileCreate):
    code_file = CodeFile(
        account_id = data.account_id,
        language = data.language,
        filepath=data.filepath,
        extension=data.extension,
    )
    db.add(code_file)
    db.commit()
    db.refresh(code_file)
    return code_file


def get_all_code_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CodeFile).offset(skip).limit(limit).all()


def get_code_file(db: Session, code_file_id: UUID):
    return db.query(CodeFile).filter(CodeFile.code_file_id == code_file_id).first()


def delete_code_file(db: Session, code_file_id: UUID):
    obj = db.query(CodeFile).filter(CodeFile.code_file_id == code_file_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
