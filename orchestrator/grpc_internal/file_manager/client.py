import grpc
from file_manager import v1_pb2_grpc, v1_pb2

def file_save(content, filename, ext = "txt"):
    channel = grpc.insecure_channel("file-manager:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.FileStub(channel)

    request = v1_pb2.FileSaveReq(
        folder="/app/scripts",
        content=content,
        filename=filename,
        ext=ext
    )

    response = stub.FileSave(request)

    return {"filepath": response.filepath}
