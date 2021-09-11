import message.status
import proc.template
import logging


class Task(proc.template.Process):
    def __init__(self, controller, task_id):
        super().__init__(controller.log_level)
        self.controller = controller
        self.task_id = task_id

    def signal(self, msg):
        self.controller.send(msg)

    def run(self):
        self.init_logging()
        try:
            self.log_begin()
            self.do_task()
            self.log_end()
            logging.info(
                "Sending task finished status message for task {}".format(
                    self.task_id
                )
            )
            self.signal(message.status.TaskFinishedMessage(self.task_id))
        except Exception as e:
            logging.error(
                "Exception occurred in task {}: {}".format(
                    self.task_id, e
                )
            )
            logging.info(
                "Sending task failed status message for task {}".format(
                    self.task_id
                )
            )
            self.signal(message.status.TaskFailedMessage(self.task_id))
        except KeyboardInterrupt:
            logging.fatal("Interrupted by keyboard: exiting")

    def do_task(self):
        raise NotImplementedError

    def log_begin(self):
        logging.info("Starting task with unimplemented logging")

    def log_end(self):
        logging.info("Finished task with unimplemented logging")
