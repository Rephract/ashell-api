from djongo import models as mongo_models

from core.constants import LogLevels, LogTypes

class Log(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    level = mongo_models.CharField(
        max_length=20,
        choices=tuple((x.value, x.name) for x in LogLevels)
    )
    message_type = mongo_models.CharField(
        max_length=20,
        choices=tuple((x.value, x.name) for x in LogTypes),
        default=LogTypes.LOG.value
    )
    message = mongo_models.TextField(max_length=1000)
    code = mongo_models.CharField(max_length=50, blank=True, null=True)
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f'{self.message}'
