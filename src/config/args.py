import argparse


def tasks_type(x):
    try:
        x = int(x)
    except Exception:
        raise argparse.ArgumentTypeError("tasks must be int")
    if x < 3:
        raise argparse.ArgumentTypeError("Minimum tasks is 3")
    return x


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
        type=tasks_type,
        default=10
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count', default=0,
    )
    return parser.parse_args()
