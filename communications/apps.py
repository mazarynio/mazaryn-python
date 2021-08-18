from django.apps import AppConfig


"""Appconfig objects store metadata for communications app"""


class CommunicationsConfig(AppConfig):
    # primary key type to add to models within communications app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communications'  # tells Django which application this configuration applies to
