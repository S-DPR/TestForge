from grpc_tools import protoc
import platform
import sys
import glob

prefix = "/app/grpc"
_, folder = "", "file_manager"
if platform.system() == "Windows":
    prefix = r"C:\Users\Glory\PycharmProjects\FastAPIProject\grpc"

proto_files = glob.glob(f'{prefix}/**/*.proto', recursive=True)
proto_files = [i.replace(prefix + "/", '') for i in proto_files]

args = [
    "",
    f"-I=/app/grpc/{folder}",
    f"--python_out=/app/{folder}/grpc",
    f"--grpc_python_out=/app/{folder}/grpc",
    *proto_files,
]
if platform.system() == "Windows":
    args = [
        "",
        f"-I=C:/Users/Glory/PycharmProjects/FastAPIProject/grpc/{folder}",
        f"--python_out=C:/Users/Glory/PycharmProjects/FastAPIProject/{folder}/grpc",
        f"--grpc_python_out=C:/Users/Glory/PycharmProjects/FastAPIProject/{folder}/grpc",
        *proto_files
    ]

protoc.main(args)
