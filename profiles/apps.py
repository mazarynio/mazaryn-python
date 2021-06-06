from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        import profiles.signals