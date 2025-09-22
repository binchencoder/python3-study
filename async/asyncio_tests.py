import asyncio
import glob
import os
from pathlib import Path

# 定义一个特殊值来表示队列结束
SENTINEL = object()


# 模拟函数
async def convert_pdf_to_markdown(pdf_path: Path):
    """将单个 PDF 文件异步转换为 Markdown."""
    print(f">>>>>>>>>>>>>>>>>>>>>>>>开始转换 PDF: {pdf_path.name}")
    # 模拟一个耗时的 I/O 操作
    await asyncio.sleep(10)
    md_path = pdf_path.with_suffix('.md')
    md_path.touch()
    print(f">>>>>>>>>>>>>>>>>>>>>>>>PDF 转换完成: {md_path.name}")
    return md_path


async def extract_tables_from_markdown(md_path: Path):
    """从单个 Markdown 文件中异步提取表格."""
    print(f"=======================开始提取表格: {md_path.name}")
    # 模拟一个耗时的 I/O 操作
    await asyncio.sleep(5)
    print(f"=======================表格提取完成: {md_path.name}")


async def producer(pdf_dir: str, pdf_queue: asyncio.Queue):
    """生产者：扫描目录并将文件放入队列."""
    all_pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    for pdf_file in all_pdfs:
        print(f"生产者：发现新文件并放入队列 -> {os.path.basename(pdf_file)}")
        await pdf_queue.put(Path(pdf_file))

    # 放入与工作者数量相同的结束信号
    for _ in range(num_workers):
        await pdf_queue.put(SENTINEL)


async def pdf_converter_worker(pdf_queue: asyncio.Queue, md_queue: asyncio.Queue):
    """消费者 A：从 PDF 队列中取出文件并转换."""
    print("消费者 A：从 PDF 队列中取出文件并转换.")
    while True:
        pdf_path = await pdf_queue.get()
        if pdf_path is SENTINEL:
            pdf_queue.task_done()
            break

        md_path = await convert_pdf_to_markdown(pdf_path)
        await md_queue.put(md_path)
        pdf_queue.task_done()

    print("PDF 转换工作者已完成。")


async def table_extractor_worker(md_queue: asyncio.Queue):
    """消费者 B：从 Markdown 队列中取出文件并提取表格."""
    print("消费者 B：从 Markdown 队列中取出文件并提取表格.")
    while True:
        md_path = await md_queue.get()
        if md_path is SENTINEL:
            md_queue.task_done()
            break

        await extract_tables_from_markdown(md_path)
        md_queue.task_done()

    print("表格提取工作者已完成。")


async def main(pdf_dir: str, num_workers: int):
    if not os.path.exists(pdf_dir):
        print(f"目录 {pdf_dir} 不存在，请检查路径。")
        return

    pdf_queue = asyncio.Queue()
    md_queue = asyncio.Queue()

    # 启动所有任务：生产者和两个消费者组
    producer_task = asyncio.create_task(producer(pdf_dir, pdf_queue))

    converter_tasks = [
        asyncio.create_task(pdf_converter_worker(pdf_queue, md_queue))
        for _ in range(num_workers)
    ]
    extractor_tasks = [
        asyncio.create_task(table_extractor_worker(md_queue))
        for _ in range(num_workers)
    ]

    # 等待生产者任务完成
    await producer_task
    print("\n生产者已完成所有文件分发。")

    # 等待所有 PDF 转换任务完成（队列中的所有项目都已处理）
    await pdf_queue.join()
    print("\n所有 PDF 转换任务已完成。")

    # 注入结束信号，让表格提取工作者退出
    for _ in range(num_workers):
        await md_queue.put(SENTINEL)

    # 等待所有表格提取任务完成
    await md_queue.join()
    print("\n所有表格提取任务已完成。")

    # 等待所有工作者任务真正结束
    await asyncio.gather(*converter_tasks, *extractor_tasks)

    print("所有文件处理完成，程序优雅退出。")


if __name__ == "__main__":
    test_dir = "/mnt/work/code/python_workspace /pdf-extractor/input"
    os.makedirs(test_dir, exist_ok=True)
    for i in range(1, 6):
        Path(os.path.join(test_dir, f"file{i}.pdf")).touch()

    num_workers = 1
    asyncio.run(main(test_dir, num_workers), debug=True)
