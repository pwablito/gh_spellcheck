import task.task as task


class SpellCheckTask(task.Task):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
