import multiprocessing as mp
import message.message
import message.task
import message.status
import error.message
import task.scrape


def queue_controller_proc(queue):
    try:
        while True:
            msg = queue.get()
            if not isinstance(msg, message.message.Message):
                raise error.message.InvalidMessageError
            elif isinstance(msg, message.task.TaskMessage):
                new_task = None
                if isinstance(msg, message.task.ScrapeTaskMessage):
                    new_task = task.scrape.ScrapeTask(queue, msg.handle)
                if new_task:
                    worker = mp.Process(target=new_task.run, args=())
                    worker.start()
                else:
                    raise Exception

            elif isinstance(msg, message.status.TerminateMessage):
                # TODO handle termination (maybe join subprocesses)
                break
            else:
                raise error.message.InvalidMessageError
    except (error.message.InvalidMessageError, KeyError):
        print("Got invalid message")
        # TODO handle error
        pass
