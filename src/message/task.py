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


class CommitTaskMessage(TaskMessage):
    def __init__(self, repo, location):
        self.repo = repo
        self.location = location


class PublishForkTaskMessage(TaskMessage):
    def __init__(self, repo, location, branch_name):
        self.repo = repo
        self.location = location
        self.branch_name = branch_name


class PullRequestTaskMessage(TaskMessage):
    def __init__(self, upstream_repo, forked_repo, location, branch):
        self.upstream_repo = upstream_repo
        self.forked_repo = forked_repo
        self.location = location
        self.branch = branch


class CleanupTaskMessage(TaskMessage):
    def __init__(self, location):
        self.location = location


class ValidateTaskMessage(TaskMessage):
    pass


class PublishTaskMessage(TaskMessage):
    pass
