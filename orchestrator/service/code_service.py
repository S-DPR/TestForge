import asyncio
import os
import uuid
from collections import defaultdict
from grpc_internal.input_generator_service import client as tc_client
from grpc_internal.execution_service import client as code_client
from grpc_internal.storage_service import client as file_client

class StreamingTracker:
    def __init__(self, total_chunks):
        self.queue = None
        self.remaining = total_chunks

    async def init(self):
        self.queue = asyncio.Queue()
        return self

    async def add_result(self, result):
        await self.queue.put(result)

    async def results(self):
        while self.remaining:
            result = await self.queue.get()
            self.remaining -= 1
            yield result


class Canceller:
    def __init__(self):
        self.status = False

    def cancel(self):
        self.status = True

    def is_cancelled(self):
        return self.status


class ProcessMetadata:
    def __init__(self, code_uuid, code1, code2):
        self.code_uuid = code_uuid
        self.code1 = code1
        self.code2 = code2
        self.code1_name = None
        self.code2_name = None
        self.lock = asyncio.Lock()
        self.kth = 0

    async def get_kth(self):
        async with self.lock:
            self.kth += 1
            return self.kth

    def get_code1_name(self):
        if self.code1_name is None:
            self.code1_name = os.path.basename(file_client.file_save(self.code1, self.code_uuid + "_1")['filepath'])
        return self.code1_name

    def get_code2_name(self):
        if self.code2_name is None:
            self.code2_name = os.path.basename(file_client.file_save(self.code2, self.code_uuid + "_2")['filepath'])
        return self.code2_name


class CodeServiceAsync:
    MAX_CONCURRENCY = 10

    def __init__(self):
        self.queue = asyncio.Queue()
        self.account_semaphores = defaultdict(lambda: asyncio.Semaphore(3))

    async def start(self):
        for _ in range(self.MAX_CONCURRENCY):
            asyncio.create_task(self.worker_loop())

    async def worker_loop(self):
        while True:
            args = await self.queue.get()
            try:
                await self._safe_run_wrapper(args)
            except Exception as e:
                print(f"[Worker Error] {e}")
            finally:
                self.queue.task_done()

    async def _safe_run_wrapper(self, args):
        sema = self.account_semaphores[args["account_id"]]
        async with sema:
            await self.run(
                account_id=args["account_id"],
                format_=args["format_"],
                # code1_language="python",
                # code2_language="python",
                time_limit=args["time_limit"],
                repeat_count=args["repeat_count"],
                tracker=args.get("tracker", None),
                canceller=args.get("canceller", None),
                metadata=args.get("metadata", None),
            )

    async def queue_push_streaming(self, format_, code1, code1_language, code2, code2_language, time_limit, repeat_count, tracker):
        account_id = str(uuid.uuid4())
        canceller = Canceller()
        # chunks = (repeat_count + 99) // 100
        # tracker = StreamingTracker(chunks)

        while repeat_count:
            pushed = min(repeat_count, 100)
            args = {
                "account_id": account_id,
                "format_": format_,
                "time_limit": time_limit,
                "repeat_count": pushed,
                "tracker": tracker,
                "canceller": canceller,
                "metadata": ProcessMetadata(str(uuid.uuid4()), code1, code2)
            }
            await self.queue.put(args)
            repeat_count -= pushed

        async for result in tracker.results():
            yield result
            if canceller.is_cancelled():
                break

    async def run(self, account_id, format_, time_limit, repeat_count, tracker, canceller, metadata):
        code1_name = metadata.get_code1_name()
        code2_name = metadata.get_code2_name()

        async for testcase_file_res in tc_client.testcase_generate_as_file(account_id, format_, repeat_count, await metadata.get_kth(), canceller):
            if canceller.is_cancelled():
                break
            input_filepath = testcase_file_res['filepath']
            input_filename = os.path.basename(input_filepath)
            input_kth = input_filename.split("_")[1].split(".")[0]
            first_output_filename = f"{metadata.code_uuid}_{input_kth}_1.out"
            second_output_filename = f"{metadata.code_uuid}_{input_kth}_2.out"

            first_output_filepath = os.path.join("/script", first_output_filename)
            second_output_filepath = os.path.join("/script", second_output_filename)
            # input_filepath = os.path.join("/script", input_filename)

            task1 = code_client.execute_code_async(account_id, code1_name, "python",
                                                   input_filepath, first_output_filepath, time_limit)
            task2 = code_client.execute_code_async(account_id, code2_name, "python",
                                                   input_filepath, second_output_filepath, time_limit)

            code1_result, code2_result = await asyncio.gather(task1, task2)
            code1_exitcode = code1_result['exitcode']
            code2_exitcode = code2_result['exitcode']

            if code1_exitcode != code2_exitcode:
                ret = f"ERROR FAILED : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
                canceller.cancel()
            elif code1_exitcode != 0:
                ret = f"ERROR BUT EQUAL : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
            else:
                ret = file_client.file_diff("/app/scripts", first_output_filename, second_output_filename)['result']
                if ret != 'EQUAL':
                    canceller.cancel()

            await tracker.add_result({"input_filename": input_filename, "diff_status": ret})
