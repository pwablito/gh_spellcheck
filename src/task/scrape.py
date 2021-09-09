import github
import task.task as task
import message.task
import message.status


class ScrapeTask(task.Task):
    def __init__(self, controller, task_id, handle, token):
        super().__init__(controller, task_id)
        self.handle = handle
        self.token = token

    def do_task(self):
        g = github.Github(self.token)
        for repo in g.get_user(self.handle).get_repos():
            self.signal(message.task.CloneTaskMessage(repo))

    def log_begin(self):
        print("Starting scrape for {}".format(self.handle))

    def log_end(self):
        print("Finished scrape for {}".format(self.handle))
