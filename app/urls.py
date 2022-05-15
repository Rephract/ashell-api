from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Cyberpylot API",
        default_version='1.0.0',
        description="API documentation of Cyberpylot",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('v1/', 
        include([
            path('campaign/', include(('campaign.api.urls', 'campaign'), namespace='campaigns')),
            path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
        ])
    ),
]
