import grpc
from code_runner import v1_pb2_grpc, v1_pb2

def run(content, ext = "txt"):
    channel = grpc.insecure_channel("code-runner:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.CodeRunnerStub(channel)

    request = v1_pb2.ExecuteCodeReq(
        code_path="/script/test.py",
        language="python",
        input_filepath=[],
        timelimit=3
    )

    response = stub.ExecuteCode(request)

    return {"filepath": response.filepath}
