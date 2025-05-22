from grpc_internal.create_testcase import client as tc_client
from grpc_internal.code_runner import client as code_client
from grpc_internal.file_manager import client as file_client

def run(format_, code1, code2, time_limit, repeat_count):
    tc = tc_client.run(format_)
    tc_path = file_client.run(tc)
    *_, code1_name = file_client.run(code1).split("/")
    *_, code2_name = file_client.run(code2).split("/")
    code1_output_path = code_client.run(code1_name, "python", tc_path, time_limit)
    code2_output_path = code_client.run(code2_name, "python", tc_path, time_limit)
    return {
        "code1": code1_output_path,
        "code2": code2_output_path,
    }
