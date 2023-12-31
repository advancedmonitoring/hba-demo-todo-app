from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WsV1Config(AppConfig):
    name = "demotodoapp.ws_v1"
    verbose_name = _("Socket app")

    def ready(self):
        try:
            import demotodoapp.ws_v1.signals.handlers  # noqa F401
        except ImportError:
            pass
