class Message:
    pass


class TaskMessage(Message):
    pass


class TaskCompletedMessage(TaskMessage):
    def __init__(self, task):
        self.task_id = task.id


class TaskFailedMessage(TaskMessage):
    def __init__(self, task, error):
        self.task_id = task.id
        self.error = error
