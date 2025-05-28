import grpc.aio
import json
from create_testcase import v1_pb2_grpc, v1_pb2

channel = grpc.aio.insecure_channel("create-testcase:50051")
async def testcase_generate(account_id, format_, repeat_count):
    stub = v1_pb2_grpc.TestcaseStub(channel)

    request = v1_pb2.CreateTestcaseReq(
        account_id=account_id,
        format=json.dumps(format_),
        repeat_count=repeat_count,
    )

    async for response in stub.CreateTestcase(request):
        yield {"output": response.output}
