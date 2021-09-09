import pygit2
import tempfile
import task.task as task
import message.task


class CloneTask(task.Task):
    def __init__(self, controller, task_id, repo):
        super().__init__(controller, task_id)
        self.repo = repo  # Github repo object
        self.destination = tempfile.mkdtemp()

    def do_task(self):
        pygit2.clone_repository(self.repo.clone_url, self.destination)
        self.signal(message.task.SpellCheckTaskMessage(self.repo, self.destination))

    def log_begin(self):
        print("Starting clone for {} into {}".format(self.repo.name, self.destination))

    def log_end(self):
        print("Finished clone for {} into {}".format(self.repo.name, self.destination))
