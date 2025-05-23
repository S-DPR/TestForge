from grpc_internal.create_testcase import client as tc_client
from grpc_internal.code_runner import client as code_client
from grpc_internal.file_manager import client as file_client
import os

def run(format_, code1, code2, time_limit, repeat_count):
    tc = tc_client.testcase_generate(format_)
    print(tc, flush=True)
    tc_path = file_client.file_save(tc['output'])
    code1_name = os.path.basename(file_client.file_save(code1)['filepath'])
    code2_name = os.path.basename(file_client.file_save(code2)['filepath'])
    code1_output_path = code_client.execute_code(code1_name, "python", tc_path, time_limit)
    code2_output_path = code_client.execute_code(code2_name, "python", tc_path, time_limit)
    return {
        "code1": code1_output_path,
        "code2": code2_output_path,
    }