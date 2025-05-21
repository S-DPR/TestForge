import grpc
from concurrent import futures
import v1_pb2, v1_pb2_grpc


class TCGenServicer(v1_pb2_grpc.TCGenServicer):
    def __init__(self):
        self.TcGenSaveRes = getattr(v1_pb2, 'TcGenSaveRes', None)

    def TCGenSave(self, request, context):
        print("요청받음!")
        return self.TcGenSaveRes(filepath="hihi")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TCGenServicer_to_server(TCGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CreateTestcase 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    # serve()
    print(dir(v1_pb2))
