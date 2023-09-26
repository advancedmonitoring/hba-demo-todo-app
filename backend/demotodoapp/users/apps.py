from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "demotodoapp.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import demotodoapp.users.signals.handlers  # noqa F401
        except ImportError:
            pass
