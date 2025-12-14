class LogLevel:
    INFO = 0
    WARNING = 1
    ERROR = 2
    DEBUG = 3

class Logger:
    def __init__(self, target_obj, ):
        self.target_obj = target_obj
        self._logs_by_level = {LogLevel.INFO: [], LogLevel.WARNING: [], LogLevel.ERROR: [], LogLevel.DEBUG: []}

    def log(self, msg: str, log_level: int):
        self._logs_by_level[log_level].append(msg)

    def get_logs(self, log_level: int):
        return self._logs_by_level[log_level]

    def get_log(self, log_level: int, line: int):
        return self._logs_by_level[log_level][line]



