from code.code import Code
from code.runner import runner
from db.code_file.schema import CodeFileCreate
from db.code_res.schema import CodeResCreate
from db.code_file import service as file_service
from db.code_res import service as res_service
from db import sessions
from db.sessions import SessionLocal


def execute(account_id, language, code_path, input_filepath, output_filepath, timelimit):
    exitcode = runner(Code(language=language, filepath=code_path), input_filepath, output_filepath, timelimit)
    code_file_create = CodeFileCreate(
        account_id = account_id,
        language = language,
        filepath = code_path,
        code = "" # 코드중복 넣는건 일단 생략해두자
    )
    code_res_create = CodeResCreate(
        input_filepath = input_filepath,
        exitcode = exitcode,
        # execute_time = timelimit,
        # memory = ,
        output_filepath = output_filepath,
    )
    file = file_service.create_code_file(SessionLocal(), code_file_create)
    res = res_service.create_code_res(SessionLocal(), code_res_create)
    return exitcode
