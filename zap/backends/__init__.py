from .base import ZapBase
from .postgresql import LocalPostgresZap
from zap.exceptions import NoBackendError


def get_backend(**kwargs):

    for backend_cls in ZapBase.__subclasses__():
        backend = backend_cls(**kwargs)
        if backend.can_zap():
            return backend

        raise NoBackendError()
