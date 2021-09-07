import message.task as task_message


class Task:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        try:
            self.do_task()
            self.queue.put(task_message.TaskCompletedMessage(self))
        except Exception as e:
            self.queue.put(task_message.TaskFailedMessage(self, e))

    def do_task(self):
        raise NotImplementedError
