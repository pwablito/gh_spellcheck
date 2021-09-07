import multiprocessing as mp
import control.queue as queue_control


def master_proc(start_handle, start_repo, threads):
    control_queue = mp.Queue()
    queue_controller_process = mp.Process(
        target=queue_control.queue_controller_proc,
        args=(control_queue,)
    )
    queue_controller_process.start()
    while True:
        message = control_queue.get()
        if message["action"] == "log":
            print(message["message"])
        elif message["action"] == "finished":
            print("Recieved finished message: terminating")
            break
        else:
            exit("Invalid message")
    queue_controller_process.join()
