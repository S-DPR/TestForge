from code.code import Code
from code.runner import runner
from db.code_file.schema import CodeFileCreate
from db.code_res.schema import CodeResCreate
from db.code_file import service as file_service
from db.code_res import service as res_service
from db import sessions
from db.sessions import SessionLocal

from db.sessions import get_db


def execute(account_id, language, code_path, input_filepath, output_filepath, timelimit, ctx):
    exitcode = runner(Code(language=language, filepath=code_path), input_filepath, output_filepath, timelimit, ctx)
    code_file_create = CodeFileCreate(
        account_id = account_id,
        language = language,
        filepath = code_path,
        code = "" # 코드중복 넣는건 일단 생략해두자
    )
    with get_db() as db:
        file = file_service.create_code_file(db, code_file_create)
    code_res_create = CodeResCreate(
        code_file_id=file.code_file_id,
        input_filepath = input_filepath,
        exitcode = exitcode,
        # execute_time = timelimit,
        # memory = ,
        output_filepath = output_filepath,
    )
    with get_db() as db:
        res = res_service.create_code_res(db, code_res_create)
    return exitcode
