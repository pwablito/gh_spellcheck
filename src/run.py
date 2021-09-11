#!/usr/bin/env python3

import config.args
import control.master as control_master
import logging


def main():
    args = config.args.get_arguments()
    log_level = logging.WARNING
    if args.verbose == 2:
        log_level = logging.INFO
    elif args.verbose == 3:
        log_level = logging.DEBUG
    elif args.verbose >= 4:
        log_level = logging.NOTSET
    logging.basicConfig(level=log_level)
    logging.debug("Starting master_proc")
    control_master.master_proc(args.handle, args.token, args.tasks, log_level)


if __name__ == "__main__":
    main()
