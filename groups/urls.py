from .views import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('', GroupViewSet)

urlpatterns = router.urls
