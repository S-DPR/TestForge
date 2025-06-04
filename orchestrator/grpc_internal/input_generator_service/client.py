import grpc.aio
import json
from input_generator_service import v1_pb2_grpc, v1_pb2

async def testcase_generate(account_id, format_, repeat_count, canceller):
    async with grpc.aio.insecure_channel("input-generator-service:50051") as channel:
        stub = v1_pb2_grpc.TestcaseStub(channel)

        request = v1_pb2.CreateTestcaseReq(
            account_id=account_id,
            format=json.dumps(format_),
            repeat_count=repeat_count,
        )

        call = stub.CreateTestcase(request)
        async for response in call:
            if canceller.is_cancelled():
                call.cancel()
                break
            yield {"output": response.output}


# import grpc.aio
# import json
# from input-generator-service import v1_pb2_grpc, v1_pb2
#
# channel = grpc.aio.insecure_channel("create-testcase:50051")
# stub = v1_pb2_grpc.TestcaseStub(channel)
#
# async def testcase_generate(account_id, format_, repeat_count):
#     request = v1_pb2.CreateTestcaseReq(
#         account_id=account_id,
#         format=json.dumps(format_),
#         repeat_count=repeat_count,
#     )
#     async for response in stub.CreateTestcase(request):
#         yield {"output": response.output}
