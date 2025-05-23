import os
import uuid

def save(folder: str, content: str, filename: str, ext: str):
    path = os.path.join(folder, filename + "." + ext)
    with open(path, "w") as f:
        f.write(content)
    return str(path)