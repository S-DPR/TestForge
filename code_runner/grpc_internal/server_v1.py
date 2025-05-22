from concurrent import futures
from code_runner import v1_pb2, v1_pb2_grpc
from code import runner, code


class TCGenServicer(v1_pb2_grpc.CodeRunnerServicer):
    def __init__(self):
        self.ExecuteCodeRes = getattr(v1_pb2, 'ExecuteCodeRes', None)

    def TCGenSave(self, request, context):
        language = request.language
        code_path = request.code_path
        input_filepath = request.input_filepath
        timelimit = request.timelimit

        result = runner.runner(code.Code("", code_path), timelimit)

        return self.ExecuteCodeRes(filepath=result)

def serve():
    server = grpc_internal.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TCGenServicer_to_server(TCGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CodeRunner 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
