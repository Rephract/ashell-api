from django.db import models


class ScenarioManager(models.Manager):
    def applicable_scenarios(self):
        return self.filter(
            email_template__isnull=False,
            landing_page__isnull=False
        )
