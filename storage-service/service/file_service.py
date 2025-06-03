import os
import uuid

def save(folder: str, content: str, filename: str, ext: str):
    path = os.path.join(folder, filename + "." + ext)
    with open(path, "w") as f:
        f.write(content)
    return str(path)

def read(folder: str, filename: str, ext: str):
    path = os.path.join(folder, filename + "." + ext)
    with open(path, "r") as f:
        return f.read()

def diff(folder, filename1, filename2):
    path1 = os.path.join(folder, filename1)
    path2 = os.path.join(folder, filename2)
    with open(path1, 'r') as f1, open(path2, 'r') as f2:
        lines1 = [line.rstrip() for line in f1.read().rstrip().splitlines() if line.strip()]
        lines2 = [line.rstrip() for line in f2.read().rstrip().splitlines() if line.strip()]
        return "EQUAL" if lines1 == lines2 else "DIFFERENT"
