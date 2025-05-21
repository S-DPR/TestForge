import os
import uuid

def save(folder: str, content: str, ext: str):
    filename = str(uuid.uuid4()) + "." + ext
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        f.write(content)
    return str(path)