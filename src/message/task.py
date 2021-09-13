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


class PublishForkTaskMessage(TaskMessage):
    def __init__(self, repo, location):
        self.repo = repo
        self.location = location


class PullRequestTaskMessage(TaskMessage):
    def __init__(self, repo, location):
        self.repo = repo
        self.location = location


class CleanupTaskMessage(TaskMessage):
    def __init__(self, location):
        self.location = location


class ValidateTaskMessage(TaskMessage):
    pass


class PublishTaskMessage(TaskMessage):
    pass
