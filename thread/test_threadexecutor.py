import concurrent.futures
import time

from concurrent.futures import ThreadPoolExecutor

openai_executor = ThreadPoolExecutor(max_workers=5,
                                     thread_name_prefix='openai_analysis')
genai_executor = ThreadPoolExecutor(max_workers=6,
                                    thread_name_prefix='genai_analysis')


def task_runner(duration, name):
    """模拟一个耗时的任务"""
    print(f"[{name}] 开始执行，预计耗时 {duration} 秒...")
    time.sleep(duration)
    result = f"任务 {name} 完成 ({duration}s)"
    print(f"[{name}] 执行完毕。")
    return result


def main_process():
    # 使用 ThreadPoolExecutor 创建线程池
    # max_workers=2 确保至少有两个线程可以同时执行任务

    print("主程序开始提交异步任务...")

    # 1. 提交第一个任务 (返回 Future 对象)
    future1 = openai_executor.submit(task_runner, 3, "A")

    # 2. 提交第二个任务 (返回 Future 对象)
    future2 = genai_executor.submit(task_runner, 5, "B")

    # 将所有 Future 对象放入列表中
    all_futures = [future1, future2]

    print("\n--- 主程序进入等待阶段，等待所有任务完成 ---")

    # 3. 使用 wait() 等待所有 Future 对象完成
    # wait() 会阻塞主线程，直到 all_futures 中的所有任务都完成
    done, not_done = concurrent.futures.wait(
        all_futures,
        timeout=None,  # 设置为 None 表示无限期等待
        return_when=concurrent.futures.ALL_COMPLETED  # 确保所有任务都完成后才返回
    )

    print("\n--- 所有异步任务已完成 ---")

    # 4. 获取结果
    results = []
    for future in done:
        try:
            # 使用 .result() 获取任务返回值（此时不会阻塞，因为任务已完成）
            results.append(future.result())
        except Exception as exc:
            results.append(f"任务执行出错: {exc}")

    print("最终结果列表:")
    for result in results:
        print(f"- {result}")

    print("\n主程序方法执行结束。")


def main_process_map():
    task_durations = [2, 4]
    task_names = ["Task_X", "Task_Y"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        print("--- 主程序提交任务并等待 ---")

        # 使用 map() 提交任务并阻塞等待所有结果
        results = executor.map(task_runner, task_durations, task_names)

        # 当 map() 返回时，所有任务已完成
        print("--- 所有任务完成 ---")
        print("最终结果列表:")
        for result in results:
            print(f"- {result}")


if __name__ == '__main__':
    main_process()
    # main_process_map()
