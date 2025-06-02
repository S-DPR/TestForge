import grpc
from storage_service import v1_pb2_grpc, v1_pb2

def file_save(content, filename, ext = "txt"):
    channel = grpc.insecure_channel("storage-service:50051")  # gRPC 서버 주소
    stub = v1_pb2_grpc.FileStub(channel)

    request = v1_pb2.FileSaveReq(
        folder="/app/scripts",
        content=content,
        filename=filename,
        ext=ext
    )

    response = stub.FileSave(request)

    return {"filepath": response.filepath}

def file_diff(folder, filename1, filename2):
    channel = grpc.insecure_channel("storage-service:50051")
    stub = v1_pb2_grpc.FileStub(channel)

    request = v1_pb2.FileDiffReq(
        folder=folder,
        filename1=filename1,
        filename2=filename2
    )
    response = stub.FileDiff(request)
    return {"result": response.result}
