import uuid

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

def save_file(filepath: str, content: str, ext: str = ".txt") -> str:
    filename = str(uuid.uuid4())
    p = f"{filepath}/{filename}.{ext}"
    with open(p, "w") as f:
        f.write(content)
    return p
