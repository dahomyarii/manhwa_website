from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manhwa_reader"

    def ready(self):
        import manhwa_reader.signals
