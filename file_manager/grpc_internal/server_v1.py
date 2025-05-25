import grpc
from concurrent import futures
from file_manager import v1_pb2, v1_pb2_grpc
from service import file_service


class TCGenServicer(v1_pb2_grpc.FileServicer):
    def __init__(self):
        self.FileSaveRes = getattr(v1_pb2, 'FileSaveRes', None)
        self.FileDiffRes = getattr(v1_pb2, 'FileDiffRes', None)

    def FileSave(self, request, context):
        folder = request.folder
        content = request.content
        filename = request.filename
        ext = request.ext

        ret = file_service.save(folder=folder, content=content, filename=filename, ext=ext)
        return self.FileSaveRes(filepath=ret)

    def FileDiff(self, request, context):
        folder = request.folder
        filename1 = request.filename1
        filename2 = request.filename2

        ret = file_service.diff(folder=folder, filename1=filename1, filename2=filename2)
        return self.FileDiffRes(result=ret)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_FileServicer_to_server(TCGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("FileManager 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
