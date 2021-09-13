import multiprocessing as mp
import random
import string
import logging
import message.task
import message.status
import error.message
import task.scrape
import task.clone
import task.spellcheck
import proc.template


class QueueController(proc.template.Process):
    def __init__(self, log_level, token, max_tasks):
        super().__init__(log_level)
        self.task_queue = mp.Queue()
        logging.debug("Created task queue")
        self.status_queue = mp.Queue()
        logging.debug("Created status queue")
        self.token = token
        self.max_tasks = max_tasks - 2  # the controller counts as 2
        logging.info(
            "Starting queue controller with a maximum of {} worker tasks".format(  # noqa
                self.max_tasks
            )
        )
        self.task_sem = mp.Semaphore(value=self.max_tasks)
        logging.info("Initialized task semaphore of size {}".format(
            self.max_tasks
        ))

    def send(self, msg):
        logging.debug("Got message, deciding queue placement")
        if isinstance(msg, message.status.StatusMessage):
            logging.debug("Inserting message into status queue")
            self.status_queue.put(msg)
        elif isinstance(msg, message.task.TaskMessage):
            logging.debug("Inserting message into task queue")
            self.task_queue.put(msg)
        else:
            raise error.message.InvalidMessageError

    def watch_status(self):
        self.init_logging()
        logging.info("Started status queue watcher")
        try:
            while True:
                logging.debug("Waiting for status message")
                status_msg = self.status_queue.get()
                logging.info("Got status message")
                if not isinstance(status_msg, message.status.StatusMessage):
                    logging.info("Got invalid message")
                    raise error.message.InvalidMessageError
                if isinstance(status_msg, message.status.TerminateMessage):
                    logging.info("Got terminate message")
                    raise NotImplementedError
                if isinstance(status_msg, message.status.TaskFinishedMessage):
                    logging.info("Got task finished message")
                    self.task_sem.release()
                    logging.debug("task_sem released")
                elif isinstance(status_msg, message.status.TaskStartedMessage):
                    logging.info("Got task started message")
                elif isinstance(status_msg, message.status.TaskFailedMessage):
                    logging.info("Got task failed message")
                    raise NotImplementedError
        except KeyboardInterrupt:
            logging.fatal("Interrupted by keyboard: exiting")

    def run(self):
        self.init_logging()
        try:
            status_watcher = mp.Process(target=self.watch_status)
            status_watcher.start()
            try:
                while True:
                    logging.debug("Waiting for task message")
                    task_msg = self.task_queue.get()
                    logging.debug("Recieved task message from queue")
                    self.task_sem.acquire()
                    logging.debug("task_sem acquired")
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
                        elif isinstance(
                            task_msg, message.task.SpellCheckTaskMessage
                        ):
                            new_task = task.spellcheck.SpellCheckTask(
                                self, new_task_id, task_msg.repo,
                                task_msg.location
                            )
                        elif isinstance(
                            task_msg, message.task.CommitTaskMessage
                        ):
                            new_task = task.commit.CommitTask(
                                self, new_task_id, task_msg.repo,
                                task_msg.location
                            )
                        elif isinstance(
                            task_msg, message.task.PublishForkTaskMessage
                        ):
                            new_task = task.fork.PublishForkTask(
                                self, new_task_id, task_msg.repo,
                                task_msg.location
                            )
                        if new_task:
                            worker = mp.Process(target=new_task.run)
                            worker.start()
                            self.status_queue.put(
                                message.status.TaskStartedMessage(new_task_id)
                            )
                        else:
                            raise error.message.InvalidMessageError
            except KeyError as e:
                logging.error("Got invalid message")
                raise e
            logging.warn("Killing status queue watcher")
            status_watcher.terminate()
        except KeyboardInterrupt:
            logging.fatal("Interrupted by keyboard: exiting")
