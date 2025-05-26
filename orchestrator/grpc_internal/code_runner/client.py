import grpc
from code_runner import v1_pb2_grpc, v1_pb2

def execute_code(code_filename, language, input_filepath, output_filepath, timelimit):
    channel = grpc.insecure_channel("code-runner:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.CodeRunnerStub(channel)

    request = v1_pb2.ExecuteCodeReq(
        code_path=f"/script/{code_filename}",
        language=language,
        input_filepath=input_filepath,
        output_filepath=output_filepath,
        timelimit=timelimit
    )

    return { "exitcode": stub.ExecuteCode(request).exitcode }
