import grpc
import json
from dacite import from_dict
from concurrent import futures
from create_testcase import v1_pb2, v1_pb2_grpc
from request.config_structs import TestcaseConfig
from request.executor import process


class TestcaseServicer(v1_pb2_grpc.TestcaseServicer):
    def __init__(self):
        self.CreateTestcaseRes = getattr(v1_pb2, 'CreateTestcaseRes', None)

    def CreateTestcase(self, request, context):
        format_ = request.format

        format_dict = json.loads(format_)
        testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)

        return self.CreateTestcaseeRes(output=process(testcase_config))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TestcaseServicer_to_server(TestcaseServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CreateTestcase 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
