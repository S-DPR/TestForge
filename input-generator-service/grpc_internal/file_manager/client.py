import grpc
from file_manager import v1_pb2_grpc, v1_pb2

def run(content, ext = "txt"):
    channel = grpc.insecure_channel("storage-service:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.FileStub(channel)

    request = v1_pb2.FileSaveReq(
        folder="/app/scripts",
        content=content,
        ext="txt"
    )

    response = stub.FileSave(request)

    return {"filepath": response.filepath}
