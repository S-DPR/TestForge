from grpc_internal.create_testcase import client as tc_client
from grpc_internal.code_runner import client as code_client
from grpc_internal.file_manager import client as file_client
import asyncio
import os
import uuid
from queue import Queue
from collections import defaultdict
import threading

class GroupTracker:
    def __init__(self, total_chunks):
        self.total = total_chunks
        self.completed = 0
        self.results = []
        self.future = asyncio.get_event_loop().create_future()
        self.lock = threading.Lock()

    def add_result(self, result):
        with self.lock:
            self.results.append(result)
            self.completed += 1
            print("[COMP]", self.completed, flush=True)
            if self.completed == self.total and not self.future.done():
                self.future.set_result(self.results)

class CodeService:
    MAX_THREAD = 5

    def __init__(self):
        self.queue = Queue()
        self.account_semaphores = defaultdict(lambda: threading.Semaphore(2))

        for i in range(self.MAX_THREAD):
            t = threading.Thread(target=self.worker_loop, daemon=True)
            t.start()

    def worker_loop(self):
        while True:
            args = self.queue.get()
            if args is None:
                break
            try:
                asyncio.run(self._safe_run_wrapper(args))
            except Exception as e:
                print(f"[Thread Error] {e}")
            finally:
                self.queue.task_done()

    async def _safe_run_wrapper(self, args):
        sema = self.account_semaphores[args["account_id"]]
        acquired = sema.acquire(blocking=False)

        if not acquired:
            await asyncio.sleep(0.1)
            self.queue.put(args)
            return

        try:
            result = await self.run(**args)
            args["tracker"].add_result(result)
        except Exception as e:
            if not args["tracker"].future.done():
                args["tracker"].future.set_exception(e)
        finally:
            sema.release()

    async def queue_push(self, format_, code1, code2, time_limit, repeat_count):
        account_id = str(uuid.uuid4()) # 임시
        chunks = (repeat_count + 99) // 100  # 100개 단위로 나눔
        tracker = GroupTracker(chunks)

        while repeat_count:
            pushed = min(repeat_count, 100)
            args = {
                "account_id": account_id,
                "format_": format_,
                "code1": code1,
                "code2": code2,
                "time_limit": time_limit,
                "repeat_count": pushed,
            }
            self.queue.put(args)
            repeat_count -= pushed
        print("[WAIT]", flush=True)
        return await tracker.future

    async def run(self, account_id, format_, code1, code2, time_limit, repeat_count):
        # account_id = str(uuid.uuid4())

        code_uuid = str(uuid.uuid4())
        code1_name = os.path.basename(file_client.file_save(code1, code_uuid + "_1")['filepath'])
        code2_name = os.path.basename(file_client.file_save(code2, code_uuid + "_2")['filepath'])
        kth = 0
        result = []
        print("[RUN]", flush=True)
        async for tc in tc_client.testcase_generate(account_id, format_, repeat_count):
            print("[TCC]", flush=True)
            kth += 1
            input_filename = f"{code_uuid}_{kth}"
            output_filename = f"{code_uuid}_{kth}"

            first_output_filename = output_filename + "_1.out"
            second_output_filename = output_filename + "_2.out"

            first_output_filepath = os.path.join("/script", first_output_filename)
            second_output_filepath = os.path.join("/script", second_output_filename)
            input_filepath = os.path.join("/script", input_filename + ".in")

            tc_path = file_client.file_save(tc['output'], input_filename, 'in')['filepath']

            task1 = asyncio.to_thread(code_client.execute_code, account_id, code1_name, "python",
                                      input_filepath, first_output_filepath, time_limit)
            task2 = asyncio.to_thread(code_client.execute_code, account_id, code2_name, "python",
                                      input_filepath, second_output_filepath, time_limit)

            code1_result, code2_result = await asyncio.gather(task1, task2)
            code1_exitcode = code1_result['exitcode']
            code2_exitcode = code2_result['exitcode']

            if code1_exitcode != code2_exitcode:
                ret = f"ERROR FAILED : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
            elif code1_exitcode != 0:
                ret = f"ERROR BUT EQUAL : code1 - {code1_exitcode}, code2 - {code2_exitcode}"
            else:
                ret = file_client.file_diff("/app/scripts", first_output_filename, second_output_filename)['result']
            result.append({ input_filename: ret })
        print("[ENDD]", flush=True)
        return result

code_service = CodeService()
