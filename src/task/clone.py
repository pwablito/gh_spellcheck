import task.task as task


class CloneTask(task.Task):
    def __init__(self, handle, repo, branch):
        super().__init__()
        self.handle = handle  # id for an organization or user
        self.repo = repo
        self.branch = branch
