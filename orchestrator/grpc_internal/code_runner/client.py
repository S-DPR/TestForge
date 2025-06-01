import grpc.aio
from code_runner import v1_pb2_grpc, v1_pb2

# 채널 전역 재사용 (꼭 한 번만 생성해서 써야 함)
# channel = grpc.aio.insecure_channel("code-runner:50051")
# stub = v1_pb2_grpc.CodeRunnerStub(channel)

async def execute_code_async(account_id, code_filename, language, input_filepath, output_filepath, timelimit):
    async with grpc.aio.insecure_channel("code-runner:50051") as channel:
        stub = v1_pb2_grpc.CodeRunnerStub(channel)
        request = v1_pb2.ExecuteCodeReq(
            account_id=account_id,
            code_path=f"/script/{code_filename}",
            language=language,
            input_filepath=input_filepath,
            output_filepath=output_filepath,
            timelimit=timelimit
        )

        response = await stub.ExecuteCode(request)
        return { "exitcode": response.exitcode }

# import grpc
# from execution-service import v1_pb2_grpc, v1_pb2
#
# def execute_code(account_id, code_filename, language, input_filepath, output_filepath, timelimit):
#     with grpc.insecure_channel("code-runner:50051") as channel:
#         stub = v1_pb2_grpc.CodeRunnerStub(channel)
#
#         request = v1_pb2.ExecuteCodeReq(
#             account_id=account_id,
#             code_path=f"/script/{code_filename}",
#             language=language,
#             input_filepath=input_filepath,
#             output_filepath=output_filepath,
#             timelimit=timelimit
#         )
#
#         return { "exitcode": stub.ExecuteCode(request).exitcode }