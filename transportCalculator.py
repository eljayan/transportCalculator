import os, sys
from threading import Thread
from application import app

def start_page():
    app.run(port=4999)

def start_browser():
    os.system("start chrome.exe /new-window http://localhost:4999")

def kill_all(controlthread, blockingthread):
    while controlthread.isAlive():
        pass
    blockingthread.is_alive = False

def main():
    t1 = Thread(target=start_page)
    t2 = Thread(target=start_browser)
    # t3 = Thread(target=kill_all, args=(t2,t1))
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()