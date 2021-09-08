import multiprocessing as mp
import control.queue as queue_control
import message.task


def master_proc(start_handle, token, threads):
    try:
        control_queue = mp.Queue()
        queue_controller_process = mp.Process(
            target=queue_control.queue_controller_proc,
            args=(control_queue,)
        )
        queue_controller_process.start()

        # Insert starting point to queue
        control_queue.put(message.task.ScrapeTaskMessage(start_handle, token))

    except KeyboardInterrupt:
        pass
    except Exception:
        print("Something went wrong.")
    finally:
        queue_controller_process.join()
    print("Finished master_proc")
