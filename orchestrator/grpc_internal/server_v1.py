import asyncio
import json
from concurrent import futures
from orchestrator import v1_pb2, v1_pb2_grpc
from service import code_service
import grpc.aio

class TestForgeServiceServicer(v1_pb2_grpc.TestForgeServiceServicer):
    def __init__(self, code_service):
        self.code_service = code_service
        self.TestExecutorReq = getattr(v1_pb2, 'TestExecutorReq', None)
        self.TestExecutorRes = getattr(v1_pb2, 'TestExecutorRes', None)

    async def TestExecutor(self, request, context):
        testcase_format = json.loads(request.testcaseFormat)
        code1 = request.code1
        code2 = request.code2
        time_limit = request.timelimit
        repeat_count = request.repeatCount

        tracker = await code_service.StreamingTracker(repeat_count).init()
        execute = lambda: self.code_service.queue_push_streaming(
            format_ = testcase_format,
            code1 = code1,
            code1_language = "python",
            code2 = code2,
            code2_language = "python",
            time_limit = time_limit,
            repeat_count = repeat_count,
            tracker = tracker
        )
        async for r in execute():
            yield self.TestExecutorRes(filename="test",diffStatus=r)


async def serve():
    server = grpc.aio.server()
    codeServiceAsync = code_service.CodeServiceAsync()
    await codeServiceAsync.start()

    v1_pb2_grpc.add_TestForgeServiceServicer_to_server(
        TestForgeServiceServicer(codeServiceAsync),
        server
    )

    server.add_insecure_port('[::]:50051')
    print("Orchestrator 서버 실행", flush=True)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
