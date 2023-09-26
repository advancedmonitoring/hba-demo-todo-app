from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiV1Config(AppConfig):
    name = "demotodoapp.api_v1"
    verbose_name = _("API")
