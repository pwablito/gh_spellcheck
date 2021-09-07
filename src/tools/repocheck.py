class RepoCheck:

    def __init__(self, repo):
        self.repo = repo
        self.has_mistakes = False

    def clone(self):
        raise NotImplementedError

    def spellcheck(self):
        raise NotImplementedError

    def publish_pr(self):
        raise NotImplementedError

    def run(self):
        self.clone()
        self.spellcheck()
        if self.has_mistakes:
            self.validate_mistakes()
            self.publish_pr()
