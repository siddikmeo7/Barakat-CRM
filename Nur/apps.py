from django.apps import AppConfig


class NurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nur'


    def ready(self):
        import Nur.signals