import logging
from core.constants import LogLevels, LogTypes


class LoggingHandler(logging.Handler):

    def emit(self, record):
        from campaign.models import Log

        level_mapping = LogLevels.get_level_mappings()
        is_debug = hasattr(record, LogTypes.DEBUG.value)
        code = getattr(record, "code", record.levelno)

        Log.objects.create(
            level=level_mapping.get(record.levelname, 'info'),
            message=self.format(record),
            code=code,
            message_type=LogTypes.DEBUG.value if is_debug else LogTypes.LOG.value
        )
