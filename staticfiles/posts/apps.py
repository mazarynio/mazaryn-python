from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Posts,Comments,Likes'
    default_auto_field = 'django.db.models.BigAutoField'
