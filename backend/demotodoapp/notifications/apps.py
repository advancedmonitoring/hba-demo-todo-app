from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "demotodoapp.notifications"
    verbose_name = _("Notifications")

    def ready(self):
        try:
            import ampire.notifications.signals.handlers
        except ImportError:
            pass
