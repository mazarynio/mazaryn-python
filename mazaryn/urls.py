"""mazaryn URL Configuration"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views  # for testing purposes


urlpatterns = [
    path("admin/", admin.site.urls),
    path('chat/', include('communications.urls')),
    path("posts/", include("posts.urls")),
    path("groups/", include("groups.urls")),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    # url(r'^auth/', include('djoser.urls.jwt')),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
