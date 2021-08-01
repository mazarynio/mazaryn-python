from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
