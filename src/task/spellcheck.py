import task.task as task


class SpellCheckTask(task.Task):
    def __init__(self, queue, location):
        super().__init__(queue)
        self.location = location
