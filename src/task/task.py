import message.status


class Task:
    def __init__(self, controller, task_id):
        self.controller = controller
        self.task_id = task_id

    def signal(self, msg):
        self.controller.send(msg)

    def run(self):
        try:
            self.log_begin()
            self.do_task()
            self.log_end()
            self.signal(message.status.TaskFinishedMessage(self.task_id))
        except Exception as e:
            # TODO add a task failure handler
            print("Exception occurred: {}".format(e))

    def do_task(self):
        raise NotImplementedError

    def log_begin(self):
        print("Starting task {}".format(self))

    def log_end(self):
        print("Finished task {}".format(self))
