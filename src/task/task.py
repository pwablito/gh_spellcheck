import message.status
import logging


class Task:
    def __init__(self, controller, task_id):
        self.controller = controller
        self.task_id = task_id

    def signal(self, msg):
        self.controller.send(msg)

    def run(self):
        try:
            logging.info("Starting task {}".format(self.task_id))
            self.do_task()
            logging.info("Finished task {}".format(self.task_id))
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
