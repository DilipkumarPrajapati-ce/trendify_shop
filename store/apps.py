from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'
    label = 'store'

    def ready(self):
        # Import signals to ensure post_migrate handlers run
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
