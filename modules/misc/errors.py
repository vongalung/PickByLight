# TERMINATING EXCEPTIONS
class Custom_Error(Exception):
    pass

class AbandonOperation(Custom_Error):
    def __init__(self):
        self.msg='Abandoning Operation!'
# END TERMINATING EXCEPTIONS

# ERROR LOGGING
def error_log(message):
    import logging
    from config.config import ERROR_LOG_PATH,ERROR_LOG_FORMAT

    logging.basicConfig(filename=ERROR_LOG_PATH,level=logging.DEBUG,format=ERROR_LOG_FORMAT)
    logging.exception(message)
# END ERROR LOGGING
