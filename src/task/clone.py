import task.task as task


class CloneTask(task.Task):
    def __init__(self, queue, repo):
        super().__init__(queue)
        self.repo = repo  # Github repo object
