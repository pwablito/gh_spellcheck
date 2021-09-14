import task.task as task
import config.github
import logging
import os
import github


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
        try:
            # Delete fork if exists
            g = github.Github(self.controller.token)
            g.get_user().get_repo(self.repo.name).delete()
            logging.info("Deleted fork of {}".format(self.repo.full_name))
        except Exception:
            logging.info("Did not delete fork of {}".format(self.repo.full_name))
        forked_repo = self.repo.create_fork()
        cmd = "cd {} && git remote add {} https://{}@github.com/{} && git push {} {}".format(
            self.repo_dir, config.github.fork_remote_name,
            self.controller.token, forked_repo.full_name,
            config.github.fork_remote_name,
            config.github.spelling_fix_branch_name
        )
        logging.debug("Executing \"{}\"".format(cmd))
        os.system(cmd)

    def log_begin(self):
        logging.info("Starting fork for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished clone for {}".format(self.repo.full_name))
