import message.message


class TaskMessage(message.message.Message):
    pass


class ScrapeTaskMessage(TaskMessage):
    def __init__(self, handle):
        self.handle = handle


class CloneTaskMessage(TaskMessage):
    def __init__(self, repo):
        self.repo = repo


class SpellCheckTaskMessage(TaskMessage):
    def __init__(self, repo, location):
        self.repo = repo
        self.location = location


class ValidateTaskMessage(TaskMessage):
    pass


class PublishTaskMessage(TaskMessage):
    pass
