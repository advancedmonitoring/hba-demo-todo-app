from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from demotodoapp.utils.process_recognizer import ProcessRecognizer


class MainConfig(AppConfig):
    name = "demotodoapp.main"
    verbose_name = _("Todos app")

    def ready(self):
        import demotodoapp.main.signals.handlers  # noqa
        ProcessRecognizer.init()
        self.init_connections()

    @staticmethod
    def init_connections():
        from demotodoapp.ws_v1.utils import Connections

        Connections.init()
