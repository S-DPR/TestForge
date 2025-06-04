import grpc
import json
from dacite import from_dict
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor, as_completed
from input_generator_service import v1_pb2, v1_pb2_grpc
from request.config_structs import TestcaseConfig
from request.executor import process, process_with_file_save


class TestcaseServicer(v1_pb2_grpc.TestcaseServicer):
    def __init__(self):
        self.CreateTestcaseRes = getattr(v1_pb2, 'CreateTestcaseRes', None)
        self.CreateTestcaseFileRes = getattr(v1_pb2, 'CreateTestcaseFileRes', None)
        self.executor = ProcessPoolExecutor(max_workers=10)

    def CreateTestcase(self, request, context):
        account_id = request.account_id
        format_ = request.format
        repeat_count = request.repeat_count

        format_dict = json.loads(format_)

        for _ in range(request.repeat_count):
            if not context.is_active():
                break
            testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
            result = process(account_id, testcase_config)
            yield v1_pb2.CreateTestcaseRes(output=result)

    def CreateTestcaseAsFile(self, request, context):
        account_id = request.account_id
        format_ = request.format
        repeat_count = request.repeat_count
        filename = request.filename

        format_dict = json.loads(format_)

        for _ in range(request.repeat_count):
            if not context.is_active():
                break
            testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
            result = process_with_file_save(account_id, testcase_config, filename)
            yield v1_pb2.CreateTestcaseFileRes(filepath=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TestcaseServicer_to_server(TestcaseServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CreateTestcase 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# import grpc
# import json
# from dacite import from_dict
# from concurrent import futures
# from concurrent.futures import ProcessPoolExecutor, as_completed
# from input-generator-service import v1_pb2, v1_pb2_grpc
# from request.config_structs import TestcaseConfig
# from request.executor import process
#
#
# class TestcaseServicer(v1_pb2_grpc.TestcaseServicer):
#     def __init__(self):
#         self.CreateTestcaseRes = getattr(v1_pb2, 'CreateTestcaseRes', None)
#
#     def CreateTestcase(self, request, context):
#         account_id = request.account_id
#         format_ = request.format
#         repeat_count = request.repeat_count
#
#         format_dict = json.loads(format_)
#
#         print("[RES]", account_id, repeat_count, flush=True)
#         with ProcessPoolExecutor(max_workers=4) as executor:
#             testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
#             futures = [executor.submit(process, account_id, testcase_config) for _ in range(repeat_count)]
#             for f in as_completed(futures):
#                 yield v1_pb2.CreateTestcaseRes(output=f.result())
#
#         # for _ in range(repeat_count):
#         #     testcase_config = from_dict(data_class=TestcaseConfig, data=format_dict)
#         #     yield self.CreateTestcaseRes(output=process(testcase_config))
#
# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     v1_pb2_grpc.add_TestcaseServicer_to_server(TestcaseServicer(), server)
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     print("CreateTestcase 서버 실행")
#     server.wait_for_termination()
#
# if __name__ == '__main__':
#     serve()
