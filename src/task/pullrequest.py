import task.task as task
import message.task
import config.github
import logging


class PullRequestTask(task.Task):
    def __init__(
        self, controller, task_id, upstream_repo,
        forked_repo, location, branch
    ):
        super().__init__(controller, task_id)
        self.upstream_repo = upstream_repo
        self.forked_repo = forked_repo
        self.location = location
        self.branch = branch

    def do_task(self):
        self.upstream_repo.create_pull(
            config.github.pr_title, config.github.pr_message,
            self.upstream_repo.default_branch,
            '{}:{}'.format(config.github.github_username, self.branch)
        )
        self.signal(message.task.CleanupTaskMessage(self.location))

    def log_begin(self):
        logging.info("Starting pull request for {}".format(
            self.forked_repo.full_name
        ))

    def log_end(self):
        logging.info("Finished pull request for {}".format(
            self.forked_repo.full_name
        ))
