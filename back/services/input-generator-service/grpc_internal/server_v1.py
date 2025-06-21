import grpc
import json
from dacite import from_dict, Config
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor, as_completed
from input_generator_service import v1_pb2, v1_pb2_grpc
from request.config_structs import TestcaseConfig
from request.executor import process
from error.exception import ConfigValueError

from log_common import get_logger

logger = get_logger(__name__)

class TestcaseServicer(v1_pb2_grpc.TestcaseServicer):
    def __init__(self):
        self.CreateTestcaseRes = getattr(v1_pb2, 'CreateTestcaseRes', None)
        self.executor = ProcessPoolExecutor(max_workers=10)

    def CreateTestcase(self, request, context):
        logger.info('테스트케이스 생성 요청 받음')
        logger.debug(request)
        account_id = request.account_id
        format_ = request.format
        repeat_count = request.repeat_count

        logger.info("테스트케이스 설정 생성 시작")
        format_dict = json.loads(format_)
        try:
            testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
        except Exception as e:
            logger.error("테스트케이스 설정 생성 실패", e)
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        logger.info("테스트케이스 설정 생성 성공")
        logger.debug(testcase_config)

        try:
            for _ in range(repeat_count):
                if not context.is_active():
                    break
                result = process(account_id, testcase_config)
                yield v1_pb2.CreateTestcaseRes(output=result)
        except ConfigValueError as e:
            logger.error("테스트케이스 생성 중 Value 에러 발생 : %s", e)
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, e.message)
        except Exception as e:
            logger.error("알 수 없는 에러 발생 : %s", e)
            context.abort(grpc.StatusCode.INTERNAL, "서버 내부 오류")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TestcaseServicer_to_server(TestcaseServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CreateTestcase 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()