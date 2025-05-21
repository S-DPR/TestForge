# import grpc
# import v1_pb2_grpc, v1_pb2
#
# def run():
#     channel = grpc.insecure_channel("localhost:50051")  # gRPC 서버 주소
#     stub = v1_pb2_grpc.TCGenStub(channel)
#
#     request = v1_pb2.TcGenSaveReq(
#         folder="/app/scripts",
#         content="print('gRPC works!')",
#         ext="txt"
#     )
#
#     response = stub.TCGenSave(request)
#
#     return {"filepath": response.filepath}
#
# run()
