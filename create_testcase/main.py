import logging
import uvicorn
from io import BytesIO

from fastapi import FastAPI
from starlette.responses import StreamingResponse

from create_testcase.request.config_structs import TestcaseConfig
from create_testcase.request.executor import process

logger = logging.getLogger("myapp")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/create/testcase")
async def create_testcase(testcase: TestcaseConfig):
    logger.info("요청 들어옴")
    result = process(testcase)
    file_like = BytesIO(result.encode("utf-8"))
    return StreamingResponse(
        file_like,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=generated.txt"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000) #
