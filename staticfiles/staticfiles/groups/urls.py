from .views import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('groups', GroupViewSet)

urlpatterns = router.urls
