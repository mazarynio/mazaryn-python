"""mazaryn URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home_view
from rest_framework.authtoken import views  # for testing purposes


urlpatterns = [
    path("admin/", admin.site.urls),
    path("profiles/", include("profiles.urls")),
    path("posts/", include("posts.urls")),
    path("groups/", include("groups.urls")),
    path("token/", views.obtain_auth_token),  # for testing purposes
    path("api-auth/", include("rest_framework.urls")),  # for testing purposes
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
