class MultiDatabaseRouter:
    """
    A router to control if database should use
    primary database or non-relational one.
    """

    nonrel_models = {'log'}

    def db_for_read(self, model, **_hints):
        """ reading model based on params """
        if model._meta.model_name in self.nonrel_models:
            return 'nonrel'
        return 'default'

    def db_for_write(self, model, **_hints):
        """ writing model based on params """
        if model._meta.model_name in self.nonrel_models:
            return 'nonrel'
        return 'default'

    def allow_migrate(self, _db, _app_label, model_name=None, **_hints):
        """ allow models of api to sql migrate in the test env """
        if _db == 'nonrel' or model_name in self.nonrel_models:
            return False
        return True
