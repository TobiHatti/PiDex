from threading import Thread
from time import sleep

def threaded_function(arg):
    for i in range(arg):
        print ("running")
        sleep(1)


if __name__ == "__main__":
    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()

    for i in range(1,10000):
        print(i)

