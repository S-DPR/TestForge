from grpc_internal.create_testcase import client as tc_client
from grpc_internal.code_runner import client as code_client
from grpc_internal.file_manager import client as file_client
import asyncio
import os
import uuid
import uuid

async def run(format_, code1, code2, time_limit, repeat_count):
    account_id = str(uuid.uuid4())

    code_uuid = str(uuid.uuid4())
    code1_name = os.path.basename(file_client.file_save(code1, code_uuid + "_1")['filepath'])
    code2_name = os.path.basename(file_client.file_save(code2, code_uuid + "_2")['filepath'])
    kth = 0
    result = []
    for repeat in range((repeat_count+99)//100): # 100번으로 나눠서 분할실행 (중간에 diff 나오면 끊기용도)
        inner_repeat_count = min(100, repeat_count-repeat*100)
        async for tc in tc_client.testcase_generate(format_, inner_repeat_count):
            kth += 1
            input_filename = f"{code_uuid}_{kth}"
            output_filename = f"{code_uuid}_{kth}"

            first_output_filename = output_filename + "_1.out"
            second_output_filename = output_filename + "_2.out"

            first_output_filepath = os.path.join("/script", first_output_filename)
            second_output_filepath = os.path.join("/script", second_output_filename)
            input_filepath = os.path.join("/script", input_filename + ".in")

            tc_path = file_client.file_save(tc['output'], input_filename, 'in')['filepath']

            task1 = asyncio.to_thread(code_client.execute_code, account_id, code1_name, "python",
                                      input_filepath, first_output_filepath, time_limit)
            task2 = asyncio.to_thread(code_client.execute_code, account_id, code2_name, "python",
                                      input_filepath, second_output_filepath, time_limit)

            code1_result, code2_result = await asyncio.gather(task1, task2)
            code1_exitcode = code1_result['exitcode']
            code2_exitcode = code2_result['exitcode']

            if code1_exitcode != code2_exitcode:
                ret = f"ERROR FAILED : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
            elif code1_exitcode != 0:
                ret = f"ERROR BUT EQUAL : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
            else:
                ret = file_client.file_diff("/app/scripts", first_output_filename, second_output_filename)['result']
            result.append({ input_filename: ret })
    return result
