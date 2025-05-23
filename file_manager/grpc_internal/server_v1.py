import grpc
from concurrent import futures
from file_manager import v1_pb2, v1_pb2_grpc
from service import file_service


class TCGenServicer(v1_pb2_grpc.FileServicer):
    def __init__(self):
        self.FileSaveRes = getattr(v1_pb2, 'FileSaveRes', None)

    def FileSave(self, request, context):
        folder = request.folder
        content = request.content
        filename = content.filename
        ext = request.ext

        print("folder:", folder)
        print("content:", content)
        print("ext:", ext)
        ret = file_service.save(folder=folder, content=content, filename=filename, ext=ext)
        return self.FileSaveRes(filepath=ret)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_FileServicer_to_server(TCGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("FileManager 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
