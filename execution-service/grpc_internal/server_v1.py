from concurrent import futures
from execution_service import v1_pb2, v1_pb2_grpc
from service import execute_code
from code.docker_container import docker_container_pool
import grpc


class CodeRunnerServicer(v1_pb2_grpc.CodeRunnerServicer):
    def __init__(self):
        self.ExecuteCodeRes = getattr(v1_pb2, 'ExecuteCodeRes', None)

    def ExecuteCode(self, request, context):
        account_id = request.account_id
        language = request.language
        code_path = request.code_path
        input_filepath = request.input_filepath
        output_filepath = request.output_filepath
        timelimit = request.timelimit

        exitcode = execute_code.execute(account_id, language, code_path, input_filepath, output_filepath, timelimit, context)
        return self.ExecuteCodeRes(exitcode=exitcode)

def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        v1_pb2_grpc.add_CodeRunnerServicer_to_server(CodeRunnerServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("CodeRunner 서버 실행")
        server.wait_for_termination()
    finally:
        docker_container_pool.cleanup()

if __name__ == '__main__':
    serve()
