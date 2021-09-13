import task.task as task
import config.github
import logging
import os


class PublishForkTask(task.Task):
    def __init__(
        self, controller, task_id, repo, repo_dir,
        branch_name=config.github.spelling_fix_branch_name
    ):
        super().__init__(controller, task_id)
        self.repo = repo  # Github repo object
        self.repo_dir = repo_dir
        self.branch_name = branch_name

    def do_task(self):
        forked_repo = self.repo.create_fork()
        os.system("cd {} && git remote add {} {} && git push {} {}".format(
            self.repo_dir, config.github.fork_remote_name,
            forked_repo.ssh_url, config.github.fork_remote_name,
            config.github.spelling_fix_branch_name
        ))

    def log_begin(self):
        logging.info("Starting fork for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished clone for {}".format(self.repo.full_name))
