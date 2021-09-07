#!/usr/bin/env python3

import argparse
import tools.repocheck


def get_args():
    parser = argparse.ArgumentParser("GitHub Spellcheck Bot")
    parser.add_argument(
        "-r", "--repo",
        help="Repository to spellcheck",
        required=True
    )
    return parser.parse_args()


def main():
    args = get_args()
    repo = args.repo  # Get PyGithub repo object instead
    tools.repocheck.RepoCheck(repo).run()


if __name__ == "__main__":
    main()
