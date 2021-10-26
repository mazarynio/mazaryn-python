"""mazaryn URL Configuration"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views as authtoken_views 


# for documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import ping

schema_view = get_schema_view(
   openapi.Info(
      title="Mazaryn",
      default_version='v1',
      description="Distributed social system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
   path('admin/doc/', include('django.contrib.admindocs.urls')),# Visibilty is to admin only
   path('admin/', admin.site.urls),
   path('ping', ping),
   path('groups/', include("groups.urls")),
   path('group/posts/', include("posts.urls")),
   path('auth/', include('djoser.urls')),
   url(r'^auth-token/', include('djoser.urls.authtoken')),
   path('friends/', include('friends.urls')),
   path('mobile-api/auth/',authtoken_views.obtain_auth_token,name="mobile_token"),# mobile token authentication endpoint  

   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
