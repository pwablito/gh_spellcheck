import task.task as task
import message.task
import logging
import textblob
import os


ignored_files = []
ignored_dirs = ['.git']
valid_endings = [
    '.py', '.js', '.html', '.css', '.md', '.txt', '.c', '.h', '.cpp'
]


class SpellCheckTask(task.Task):
    def __init__(self, controller, task_id, repo, location):
        super().__init__(controller, task_id)
        self.repo = repo
        self.location = location
        self.changes = False

    def do_task(self):
        self.correct_dir(self.location)
        if self.changes:
            logging.info(
                "Spelling changes found, signalling for commit"
            )
            self.signal(
                message.task.CommitTaskMessage(self.repo, self.location)
            )
        else:
            self.signal(message.task.CleanupTaskMessage(
                self.repo, self.location
            ))
            logging.info("No spelling changes found, signalling for cleanup")

    def correct_dir(self, location):
        for file in self.files_in_directory(location):
            logging.debug("Correcing spelling changes in file {}".format(file))
            self.correct_file(file)
        for directory in self.dirs_in_directory(location):
            logging.debug("Correcting spelling changes in directory {}".format(
                directory
            ))
            self.correct_dir(directory)

    def files_in_directory(self, directory):
        files = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                for ending in valid_endings:
                    if file.endswith(ending):
                        files.append(os.path.join(directory, file))
                        break
        return files

    def dirs_in_directory(self, directory):
        dirs = []
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                if os.path.basename(file) not in ignored_dirs:
                    dirs.append(os.path.join(directory, file))
        return dirs

    def correct_file(self, filename):
        f = open(filename, "r")
        content = f.read()
        corrected_content = textblob.TextBlob(content).correct()
        if corrected_content != content:
            self.changes = True
        f.close()
        f = open(filename, "w")
        f.write(str(corrected_content))
        f.close()

    def log_begin(self):
        logging.info("Starting spellcheck for {}".format(self.repo.full_name))

    def log_end(self):
        logging.info("Finished spellcheck for {}".format(self.repo.full_name))
