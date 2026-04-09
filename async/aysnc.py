import asyncio
import time

loop = asyncio.get_event_loop()


async def coroutine_function():
    # await asyncio.sleep(2)
    time.sleep(2)
    print('Hello, World!')


async def main():
    task = loop.create_task(coroutine_function())
    # await task

print("before loop.run_until_complete(main())")
loop.run_until_complete(main())
print("after loop.run_until_complete(main())")
