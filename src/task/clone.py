import pygit2
import tempfile
import task.task as task
import message.task


class CloneTask(task.Task):
    def __init__(self, queue, repo):
        super().__init__(queue)
        self.repo = repo  # Github repo object
        self.destination = tempfile.mkdtemp()

    def do_task(self):
        pygit2.clone_repository(self.repo.clone_url, self.destination)
        self.queue.put(message.task.SpellCheckTaskMessage(self.repo, self.destination))

    def log_begin(self):
        print("Starting clone for {} into {}".format(self.repo.name, self.destination))

    def log_end(self):
        print("Finished clone for {} into {}".format(self.repo.name, self.destination))
