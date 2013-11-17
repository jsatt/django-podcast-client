from __future__ import absolute_import


try:
    from .celery import app
except ImportError:
    pass
