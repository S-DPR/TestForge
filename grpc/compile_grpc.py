from grpc_tools import protoc
import platform
import sys
import glob

prefix = "/app/grpc"
_, folder, *_ = *sys.argv, 0
if platform.system() == "Windows":
    prefix = r"C:\Users\dev\PycharmProjects\TestForge\grpc"
    folder = "auth"

proto_files = glob.glob(f'{prefix}/**/*.proto', recursive=True)

print(proto_files)

args = [
    "",
    f"-I=/app/grpc",
    f"--python_out=/app/{folder}/grpc_internal",
    f"--grpc_python_out=/app/{folder}/grpc_internal",
    *proto_files
]
if platform.system() == "Windows":
    args = [
        "",
        f"-I=C:/Users/dev/PycharmProjects/TestForge/grpc",
        f"--python_out=C:/Users/dev/PycharmProjects/TestForge/{folder}/grpc_internal",
        f"--grpc_python_out=C:/Users/dev/PycharmProjects/TestForge/{folder}/grpc_internal",
        *proto_files
    ]

protoc.main(args)
