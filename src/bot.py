import argparse


def get_args():
    parser = argparse.ArgumentParser("GitHub Spellcheck Bot")
    parser.add_argument("-r", "--repo", help="Repository to spellcheck")
    return parser.parse_args()


def main():
    args = get_args()
    print(args)


if __name__ == "__main__":
    main()
