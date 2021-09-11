import logging


class Process:
    # Template class for a process with logging enabled
    def __init__(self, log_level):
        self.log_level = log_level

    def init_logging(self):
        logging.basicConfig(level=self.log_level)