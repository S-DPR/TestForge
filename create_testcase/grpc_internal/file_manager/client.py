import grpc
from file_manager import v1_pb2_grpc, v1_pb2

def run(content, ext = "txt"):
    channel = grpc.insecure_channel("file-manager:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.TCGenStub(channel)

    request = v1_pb2.TcGenSaveReq(
        folder="/app/scripts",
        content=content,
        ext="txt"
    )

    response = stub.TCGenSave(request)

    return {"filepath": response.filepath}
