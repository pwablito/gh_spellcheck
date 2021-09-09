import multiprocessing as mp
import random
import string
import message.task
import message.status
import error.message
import task.scrape
import task.clone


class QueueController:
    def __init__(self, token, max_tasks):
        self.task_queue = mp.Queue()
        self.status_queue = mp.Queue()
        self.token = token
        self.max_tasks = max_tasks - 2  # because the controller itself counts as 2
        self.task_sem = mp.Semaphore(value=self.max_tasks)

    def send(self, msg):
        if isinstance(msg, message.status.StatusMessage):
            self.status_queue.put(msg)
        elif isinstance(msg, message.task.TaskMessage):
            self.task_queue.put(msg)
        else:
            raise error.message.InvalidMessageError

    def watch_status(self):
        while True:
            # print("Available task slots: {}".format(self.task_sem))
            status_msg = self.status_queue.get()
            if not isinstance(status_msg, message.status.StatusMessage):
                raise error.message.InvalidMessageError
            if isinstance(status_msg, message.status.TerminateMessage):
                # TODO handle termination (maybe join subprocesses)
                raise NotImplementedError
            self.task_sem.release()

    def run(self):
        status_watcher = mp.Process(target=self.watch_status)
        status_watcher.start()
        try:
            while True:
                task_msg = self.task_queue.get()
                self.task_sem.acquire()
                if not isinstance(task_msg, message.task.TaskMessage):
                    raise error.message.InvalidMessageError
                else:
                    new_task = None
                    new_task_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                    if isinstance(task_msg, message.task.ScrapeTaskMessage):
                        new_task = task.scrape.ScrapeTask(self, new_task_id, task_msg.handle, self.token)
                    elif isinstance(task_msg, message.task.CloneTaskMessage):
                        new_task = task.clone.CloneTask(self, new_task_id, task_msg.repo)
                    if new_task:
                        worker = mp.Process(target=new_task.run, args=())
                        worker.start()
                    else:
                        raise Exception
        except (error.message.InvalidMessageError, KeyError):
            print("Got invalid message")
            # TODO handle error
            pass
        status_watcher.terminate()
