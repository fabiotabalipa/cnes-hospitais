DEBUG_LEVEL = "Debug"
ERROR_LEVEL = "Error"
INFO_LEVEL = "Info"
WARNING_LEVEL = "Warning"


class Logger:
    @staticmethod
    def debug(msg):
        Logger.__output(DEBUG_LEVEL, msg)

    @staticmethod
    def error(error):
        Logger.__output(ERROR_LEVEL, str(error))

    @staticmethod
    def info(msg):
        Logger.__output(INFO_LEVEL, msg)

    @staticmethod
    def warning(msg):
        Logger.__output(WARNING_LEVEL, msg)

    @staticmethod
    def __output(level, msg):
        print(level, "-", msg)
