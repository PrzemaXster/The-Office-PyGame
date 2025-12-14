from service.Logging.Logger import Logger


class LoggerFactory:
    def __init__(self):
        self.loggers = {}

    def get_logger(self, target_obj):
        if self.loggers.__contains__(target_obj):
            logger = self.loggers[target_obj]
        else:
            logger = Logger(target_obj)
            self.loggers[target_obj] = logger
        return logger
