import argparse


def get_arguments():
    parser = argparse.ArgumentParser("GitHub Spellcheck Bot")
    parser.add_argument(
        "--handle",
        help="Handle for repository",
        required=True
    )
    parser.add_argument(
        "--token",
        help="Access token for Github",
        required=True
    )
    parser.add_argument(
        "--tasks",
        help="Maximum tasks to run at once",
        type=int,
        default=10
    )
    return parser.parse_args()
