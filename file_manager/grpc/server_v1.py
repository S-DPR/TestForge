import grpc
from concurrent import futures
from grpc.file_manager import v1_pb2, v1_pb2_grpc
from service import file_service


class TCGenServicer(v1_pb2_grpc.TCGenServicer):
    def __init__(self):
        self.TcGenSaveRes = getattr(v1_pb2, 'TcGenSaveRes', None)

    def TCGenSave(self, request, context):
        folder = request.folder
        content = request.content
        ext = request.ext

        print("folder:", folder)
        print("content:", content)
        print("ext:", ext)
        ret = file_service.save(folder=folder, content=content, ext=ext)
        return self.TcGenSaveRes(filepath=ret)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_TCGenServicer_to_server(TCGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("FileManager 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
