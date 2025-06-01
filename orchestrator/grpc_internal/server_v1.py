from concurrent import futures
from orchestrator import v1_pb2, v1_pb2_grpc
from service import code_service
import grpc


class TestForgeServiceServicer(v1_pb2_grpc.TestForgeServiceServicer):
    def __init__(self):
        self.TestExecutorReq = getattr(v1_pb2, 'TestExecutorReq', None)

    async def TestExecutor(self, request, context):
        testcase_format = request.testcaseFormat
        code1 = request.code1
        code1_language = request.code1Language
        code2 = request.code2
        code2_language = request.code2Language
        time_limit = request.timelimit
        repeat_count = request.repeatCount

        execute = lambda: code_service.code_service.queue_push_streaming(
            format_ = testcase_format,
            code1 = code1,
            code1_language = code1_language,
            code2 = code2,
            code2_language = code2_language,
            time_limit = time_limit,
            repeat_count = repeat_count
        )
        async for r in execute():
            yield r

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TestForgeServiceServicer_to_server(TestForgeServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Orchestrator 서버 실행", flush=True)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
