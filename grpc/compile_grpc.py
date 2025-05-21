from grpc_tools import protoc
import platform
import sys
import glob

prefix = "/app/grpc"
_, folder = sys.argv
if platform.system() == "Windows":
    prefix = r"C:\Users\Glory\PycharmProjects\FastAPIProject\grpc"

proto_files = glob.glob(f'{prefix}/**/*.proto', recursive=True)

print(proto_files)

args = [
    "",
    f"-I=/app/grpc",
    f"--python_out=/app/{folder}/grpc",
    f"--grpc_python_out=/app/{folder}/grpc",
    *proto_files
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