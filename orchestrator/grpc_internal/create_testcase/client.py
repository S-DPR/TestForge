import grpc
import json
from create_testcase import v1_pb2_grpc, v1_pb2

def testcase_generate(format_):
    channel = grpc.insecure_channel("create-testcase:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.TestcaseStub(channel)

    request = v1_pb2.CreateTestcaseReq(
        format=json.dumps(format_)
    )

    response = stub.CreateTestcase(request)

    return {"output": response.output}
