from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Probe Fab API",
        default_version='v1',
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_notification.urls')),
    url('swagger/$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui')
]
