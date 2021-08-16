from .views import *
from rest_framework import routers
from django.urls import re_path, include


router = routers.DefaultRouter()

router.register('', GroupViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
]
