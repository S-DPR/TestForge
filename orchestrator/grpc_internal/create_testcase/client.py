import grpc
from create_testcase import v1_pb2_grpc, v1_pb2

def run(format_):
    channel = grpc.insecure_channel("create-testcase:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.CodeRunnerStub(channel)

    request = v1_pb2.ExecuteCodeReq(
        format=format_
    )

    response = stub.ExecuteCode(request)

    return {"output": response.output}
