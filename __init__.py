import threading
import time
def print_func(delay):
    time.sleep(delay)
    li.append("0")
    print("hi")


if __name__ == "__main__":
    li = []
    thread_1 = threading.Thread(target=print_func, args=[2])
    thread_2 = threading.Thread(target=print_func, args=[3])
    thread_1.start()
    thread_1.join()
    thread_2.start()
    thread_2.join()
    print(li)
