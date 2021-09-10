#!/usr/bin/env python3

import config.args
import control.master as control_master
import logging


def main():
    args = config.args.get_arguments()
    if args.verbose > 0:
        if args.verbose == 1:
            logging.basicConfig(level=logging.WARNING)
        elif args.verbose == 2:
            logging.basicConfig(level=logging.INFO)
        elif args.verbose == 3:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.NOTSET)
    logging.debug("Starting master_proc")
    control_master.master_proc(args.handle, args.token, args.tasks)


if __name__ == "__main__":
    main()
