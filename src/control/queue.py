import message.message
import message.task
import message.status
import error.message


def queue_controller_proc(queue):
    try:
        while True:
            msg = queue.get()
            if not isinstance(msg, message.message.Message):
                raise error.message.InvalidMessageError
            if isinstance(msg, message.task.TaskMessage):
                # TODO Dispatch task -- handle suboptions
                pass
            if isinstance(msg, message.status.TerminateMessage):
                # TODO handle termination (maybe join subprocesses)
                break
            else:
                raise error.message.InvalidMessageError
    except (error.message.InvalidMessageError, KeyError):
        # TODO handle error
        pass
