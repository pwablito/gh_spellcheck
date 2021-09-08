import multiprocessing as mp
import control.queue as queue_control
import message.task


def master_proc(start_handle, token, threads):
    try:
        control_queue = mp.Queue()
        queue_controller_process = mp.Process(
            target=queue_control.queue_controller_proc,
            args=(control_queue, token,)
        )
        queue_controller_process.start()

        # Insert starting point to queue
        control_queue.put(message.task.ScrapeTaskMessage(start_handle))

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Something went wrong: {}".format(e))
    finally:
        queue_controller_process.join()
    print("Finished master_proc")
