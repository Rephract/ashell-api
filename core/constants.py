from enum import Enum


class LogLevels(Enum):
    DEBUG = "debug"
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"

    @staticmethod
    def get_level_mappings():
        return {level.name:level.value for level in LogLevels}


class LogTypes(Enum):
    LOG = "log"
    DEBUG = "debug"
