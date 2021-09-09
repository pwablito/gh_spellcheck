import task.task as task


class SpellCheckTask(task.Task):
    def __init__(self, controller, task_id, location):
        super().__init__(controller, task_id)
        self.location = location
