import multiprocessing as mp
import control.queue as queue_control
import message.task
import logging


def master_proc(start_handle, token, threads, log_level):
    try:
        controller = queue_control.QueueController(log_level, token, threads)
        queue_controller_process = mp.Process(
            target=controller.run,
            args=()
        )
        queue_controller_process.start()

        # Insert starting point to queue
        logging.info("Sending initial message to queue controller")
        controller.send(message.task.ScrapeTaskMessage(start_handle))

    except KeyboardInterrupt:
        logging.fatal("Interrupted by keyboard: exiting")
    finally:
        queue_controller_process.join()
    logging.debug("Exiting master_proc")
