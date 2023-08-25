from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MobileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mobiles"
    verbose_name = _("Mobile app")

    def ready(self):
        pass
