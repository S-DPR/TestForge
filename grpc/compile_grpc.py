from grpc_tools import protoc
import platform
import sys

_, folder, version, *_ = (*sys.argv, 0, 0)
if not folder:
    folder = "create_testcase"
if not version:
    version = "v1"

args = [
    "",
    f"-I=/app/grpc/{folder}",
    f"--python_out=/app/{folder}/grpc",
    f"--grpc_python_out=/app/{folder}/grpc",
    f"/app/grpc/{folder}/{version}.proto",
]
if platform.system() == "Windows":
    args = [
        "",
        f"-I=C:/Users/Glory/PycharmProjects/FastAPIProject/grpc/{folder}",
        f"--python_out=C:/Users/Glory/PycharmProjects/FastAPIProject/{folder}/grpc",
        f"--grpc_python_out=C:/Users/Glory/PycharmProjects/FastAPIProject/{folder}/grpc",
        rf"C:\Users\Glory\PycharmProjects\FastAPIProject\grpc\{folder}\{version}.proto"
    ]

protoc.main(args)
