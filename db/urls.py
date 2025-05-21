from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 架构视图配置
schema_view = get_schema_view(
    openapi.Info(
        title="API 文档",
        default_version='v1',
        description="接口文档描述",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 原始 JSON/YAML
    path('swagger.json', schema_view.without_ui(cache_timeout=0),  # OpenAPI JSON
         path('swagger.yaml', schema_view.without_ui(cache_timeout=0),  # OpenAPI YAML
]