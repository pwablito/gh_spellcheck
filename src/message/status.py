import message.message


class StatusMessage(message.message.Message):
    pass


class TerminateMessage(StatusMessage):
    pass


class TaskFinishedMessage(StatusMessage):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id


class TaskFailedMessage(StatusMessage):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id


class ScrapeFinishedMessage(TaskFinishedMessage):
    pass
