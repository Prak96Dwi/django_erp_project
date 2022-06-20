from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    """
    core app configuration class
    """
    name = 'apps.user'
    verbose_name = _('user')

    def ready(self):
        import apps.user.signals  # noqa
