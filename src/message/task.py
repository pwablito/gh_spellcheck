import message.message


class TaskMessage(message.message.Message):
    pass


class ScrapeTaskMessage(TaskMessage):
    def __init__(self, handle):
        self.handle = handle


class CloneTaskMessage(TaskMessage):
    def __init__(self, repo):
        self.repo = repo


class SpellcheckTaskMessage(TaskMessage):
    def __init__(self, handle, repo_name, location):
        self.handle = handle
        self.repo_name = repo_name
        self.location = location


class ValidateTaskMessage(TaskMessage):
    # TODO figure out how to implement this- should it send an email and wait for approval?
    pass


class PublishTaskMessage(TaskMessage):
    pass
