import uuid

from confluent_kafka import Producer

def save_file(folder: str, content: str, ext: str = ".txt") -> dict[str, str]:
    filename = str(uuid.uuid4())
    p = f"{folder}/{filename}.{ext}"
    with open(p, "w") as f:
        f.write(content)
    return {
        "filepath": p
    }
