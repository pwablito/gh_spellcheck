import multiprocessing as mp
import random
import string
import logging
import message.task
import message.status
import error.message
import task.scrape
import task.clone


class QueueController:
    def __init__(self, token, max_tasks):
        self.task_queue = mp.Queue()
        logging.debug("Created task queue")
        self.status_queue = mp.Queue()
        logging.debug("Created status queue")
        self.token = token
        self.max_tasks = max_tasks - 2  # the controller counts as 2
        logging.info(
            "Starting queue controller with a maximum of {} worker threads".format(  # noqa
                self.max_tasks
            )
        )
        self.task_sem = mp.Semaphore(value=self.max_tasks)
        logging.info("Initialized task semaphore of size {}".format(
            self.max_tasks
        ))

    def send(self, msg):
        if isinstance(msg, message.status.StatusMessage):
            logging.debug("Inserting message into status queue")
            self.status_queue.put(msg)
        elif isinstance(msg, message.task.TaskMessage):
            logging.debug("Inserting message into task queue")
            self.task_queue.put(msg)
        else:
            raise error.message.InvalidMessageError

    def watch_status(self):
        logging.info("Started status queue watcher")
        try:
            while True:
                status_msg = self.status_queue.get()
                logging.info("Got status message")
                if not isinstance(status_msg, message.status.StatusMessage):
                    logging.info("Got invalid message")
                    raise error.message.InvalidMessageError
                if isinstance(status_msg, message.status.TerminateMessage):
                    logging.info("Got terminate message")
                    raise NotImplementedError
                self.task_sem.release()
                logging.debug("task_sem released")
        except KeyboardInterrupt:
            logging.fatal("Interrupted by keyboard: exiting")

    def run(self):
        try:
            status_watcher = mp.Process(target=self.watch_status)
            status_watcher.start()
            try:
                while True:
                    task_msg = self.task_queue.get()
                    self.task_sem.acquire()
                    if not isinstance(task_msg, message.task.TaskMessage):
                        logging.error("Got invalid message: {}".format(
                            task_msg
                        ))
                    else:
                        new_task = None
                        new_task_id = ''.join(
                            random.choice(
                                string.ascii_uppercase + string.digits
                            ) for _ in range(10)
                        )
                        if isinstance(
                            task_msg, message.task.ScrapeTaskMessage
                        ):
                            new_task = task.scrape.ScrapeTask(
                                self, new_task_id, task_msg.handle, self.token
                            )
                        elif isinstance(
                            task_msg, message.task.CloneTaskMessage
                        ):
                            new_task = task.clone.CloneTask(
                                self, new_task_id, task_msg.repo
                            )
                        if new_task:
                            worker = mp.Process(target=new_task.run, args=())
                            worker.start()
                        else:
                            raise Exception
            except KeyError:
                logging.error("Got invalid message")
            status_watcher.terminate()
        except KeyboardInterrupt:
            logging.fatal("Interrupted by keyboard: exiting")
