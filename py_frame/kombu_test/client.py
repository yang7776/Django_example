
from py_frame.kombu_test.kombu_client import KombuClient
from py_frame.microservice.app import run
import time
import psutil
from multiprocessing import Process

def a(msg):
    # with open(os.path.join(os.getcwd(),'stop.txt'), 'r') as f:
    #     is_stop = f.read()
    #     if is_stop == "stop":
    #         client.should_stop = True  # 停止kombu监控的字段
    time.sleep(1)
    print(f"___正在执行____{msg}____{psutil.Process()}___{psutil.Process().children(recursive=True)}")

def run_k():
    queue = 'video'
    client = KombuClient(a, queue, "redis://localhost:6379/1")
    client.start_consuming()

if __name__ == '__main__':
    f_list = [run, run_k]
    for i in f_list:
        p = Process(target=i)
        p.start()


