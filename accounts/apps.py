from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # import signals to auto-create profiles
        try:
            import accounts.signals  # noqa: F401
        except Exception:
            pass
