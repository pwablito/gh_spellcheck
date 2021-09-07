import time


def queue_controller_proc(queue):
    time.sleep(3)
    queue.put({
        "action": "log",
        "message": "message 1"
    })
    time.sleep(2)
    queue.put({
        "action": "finished"
    })
