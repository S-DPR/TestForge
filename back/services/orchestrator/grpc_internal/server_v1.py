import asyncio
import json
from orchestrator import v1_pb2, v1_pb2_grpc
from service import code_service
import grpc.aio

from log_common import get_logger

from error.exception import CreateTestcaseError

logger = get_logger(__name__)

class TestForgeServiceServicer(v1_pb2_grpc.TestForgeServiceServicer):
    def __init__(self, code_service):
        self.code_service = code_service
        self.TestExecutorReq = getattr(v1_pb2, 'TestExecutorReq', None)
        self.TestExecutorRes = getattr(v1_pb2, 'TestExecutorRes', None)

    async def TestExecutor(self, request, context):
        logger.info("TestExecutor 요청 받음")
        logger.debug(request)
        testcase_format = json.loads(request.testcaseFormat)
        code1 = request.code1
        code1_language = request.code1Language
        code2 = request.code2
        code2_language = request.code2Language
        time_limit = request.timelimit
        repeat_count = request.repeatCount

        try:
            tracker = await code_service.StreamingTracker(repeat_count).init()
            execute = lambda: self.code_service.queue_push_streaming(
                format_ = testcase_format,
                code1 = code1,
                code1_language = code1_language,
                code2 = code2,
                code2_language = code2_language,
                time_limit = time_limit,
                repeat_count = repeat_count,
                tracker = tracker
            )
            async for ret in execute():
                yield self.TestExecutorRes(filename=ret.filename,diffStatus=ret.diff_status)
        except CreateTestcaseError as e:
            logger.exception("테스트케이스 생성 중 에러 발생")
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, e.details)
            yield self.TestExecutorRes(filename="", diffStatus="ERROR" + e.details)
        except Exception as e:
            logger.exception("🔥 내부 예외 발생")
            context.abort(grpc.StatusCode.INTERNAL, "서버 내부 오류")
            yield self.TestExecutorRes(filename="", diffStatus="ERROR" + str(e))


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