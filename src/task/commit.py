import task.task as task
import message.task
import config.github
import logging
import os
from datetime import datetime


class CommitTask(task.Task):
    def __init__(self, controller, task_id, repo, location):
        super().__init__(controller, task_id)
        self.repo = repo
        self.location = location
        self.branch_name = config.github.spelling_fix_branch_name + "-" + datetime.now().strftime("%d-%m-%Y-%H%M%S")

    def do_task(self):
        os.system(
            "cd {} && git checkout -b {} && git config --local user.name \"{}\" && git config --local user.email \"{}\" && git commit -am \"{}\"".format(  # noqa
                self.location,
                self.branch_name,
                config.github.commit_name,
                config.github.commit_email,
                config.github.commit_message
            )
        )
        self.signal(message.task.PublishForkTaskMessage(self.repo, self.location, self.branch_name))

    def log_begin(self):
        logging.info("Starting spellcheck for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished spellcheck for {}".format(self.repo.full_name))
