from django.conf import settings


class ZapBase(object):

    def __init__(self, database='default', **kwargs):
        self.engine = settings.DATABASES[database]['ENGINE']
        self.name = settings.DATABASES[database]['NAME']
        self.user = settings.DATABASES[database]['USER']
        self.password = settings.DATABASES[database]['PASSWORD']
        self.host = settings.DATABASES[database]['HOST']
        self.port = settings.DATABASES[database]['PORT']
        self.debug = settings.DEBUG
        self.database = database
        self.kwargs = kwargs

    def can_zap(self):
        return False

    def zap_user(self):
        raise NotImplementedError(self.zap_user)

    def zap_db(self):
        raise NotImplementedError(self.zap_db)

    def create_user(self):
        raise NotImplementedError(self.create_user)

    def create_db(self):
        raise NotImplementedError(self.create_db)
