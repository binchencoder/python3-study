import time
from concurrent.futures import ThreadPoolExecutor


def test(times):
    time.sleep(times)
    print("over_test")


t = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
t.submit(test, times=2)

print('over')
