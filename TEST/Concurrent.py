import concurrent.futures
import random
import time


def foo(bar):
    i = random.random()
    time.sleep(i)
    return bar


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    to_do = []
    for i in range(10):  # 模拟多个任务
        future = executor.submit(foo, f"hello world! {i}")
        to_do.append(future)

    for future in concurrent.futures.as_completed(to_do):  # 并发执行
        print(future.result())
