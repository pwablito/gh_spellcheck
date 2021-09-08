import github
import task.task as task
import message.task


class ScrapeTask(task.Task):
    def __init__(self, queue, handle, token):
        super().__init__(queue)
        self.handle = handle
        self.token = token

    def do_task(self):
        print("Scraping https://github.com/{}".format(self.handle))
        g = github.Github(self.token)
        for repo in g.get_user(self.handle).get_repos():
            self.queue.put(message.task.CloneTaskMessage(self.handle, repo.name))

    def log_begin(self):
        print("Starting scrape for {}".format(self.handle))

    def log_end(self):
        print("Finished scrape for {}".format(self.handle))
