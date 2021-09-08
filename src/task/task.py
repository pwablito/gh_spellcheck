import message.task as task_message


class Task:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        try:
            self.log_begin()
            self.do_task()
            self.log_end()
        except Exception as e:
            # TODO add a task failure handler
            print("Exception occurred: {}".format(e))

    def do_task(self):
        raise NotImplementedError

    def log_begin(self):
        print("Starting task {}".format(self))

    def log_end(self):
        print("Finished task {}".format(self))
