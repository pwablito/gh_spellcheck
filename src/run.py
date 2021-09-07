#!/usr/bin/env python3

import config.args
import control.master as control_master


def main():
    args = config.args.get_arguments()
    control_master.master_proc(args.handle, args.repo, args.tasks)


if __name__ == "__main__":
    main()
