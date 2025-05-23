from concurrent import futures
from code_runner import v1_pb2, v1_pb2_grpc
from code.code import Code
from code.runner import runner
import grpc


class CodeRunnerServicer(v1_pb2_grpc.CodeRunnerServicer):
    def __init__(self):
        self.ExecuteCodeRes = getattr(v1_pb2, 'ExecuteCodeRes', None)

    def ExecuteCode(self, request, context):
        language = request.language
        code_path = request.code_path
        input_filepath = request.input_filepath
        output_filepath = request.output_filepath
        timelimit = request.timelimit

        return self.ExecuteCodeRes(exitcode=runner(Code(language=language, filepath=code_path), input_filepath, output_filepath, timelimit))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_CodeRunnerServicer_to_server(CodeRunnerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CodeRunner 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
