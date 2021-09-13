import task.task as task
import message.task
import config.github
import logging
import os


class CommitTask(task.Task):
    def __init__(self, controller, task_id, repo, location):
        super().__init__(controller, task_id)
        self.repo = repo
        self.location = location

    def do_task(self):
        os.system(
            "cd {} && git checkout -b {} && git commit -a --author=\"{} <{}>\" -m \"{}\"".format(  # noqa
                self.location,
                config.github.spelling_fix_branch_name,
                config.github.commit_name,
                config.github.commit_email,
                config.github.commit_message
            )
        )
        self.signal(message.task.PublishForkTaskMessage(self.repo, self.location))

    def log_begin(self):
        logging.info("Starting spellcheck for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished spellcheck for {}".format(self.repo.full_name))
