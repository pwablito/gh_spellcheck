import task.task as task
import logging
import textblob
import os


class SpellCheckTask(task.Task):
    def __init__(self, controller, task_id, repo, location):
        super().__init__(controller, task_id)
        self.repo = repo
        self.location = location

    def do_task(self):
        self.correct_dir(self.location)

    def correct_dir(self, location):
        for file in self.files_in_directory(location):
            logging.info("Correcing spelling changes in file {}".format(file))
            self.correct_file(file)
        for directory in self.dirs_in_directory(location):
            logging.info("Correcting spelling changes in directory {}".format(
                directory
            ))
            self.correct_dir(directory)

    def files_in_directory(self, directory):
        files = []
        for file in os.listdir(directory, hidden=True):
            if os.path.isfile(os.path.join(directory, file)):
                files.append(os.path.join(directory, file))
        return files

    def dirs_in_directory(self, directory):
        dirs = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                dirs.append(os.path.join(directory, file))
        return dirs

    def correct_file(self, filename):
        f = open(filename, "r")
        content = f.read()
        corrected_content = textblob.TextBlob(content).correct()
        f.write(corrected_content)

    def log_begin(self):
        logging.info("Starting spellcheck for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished spellcheck for {}".format(self.repo.full_name))
