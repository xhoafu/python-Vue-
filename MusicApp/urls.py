"""
URL configuration for MusicApp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from users.views import Login

# Swagger 文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="MusicApp API",
        default_version='v1',
        description="音乐应用接口文档",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="dev@musicapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),

    # API 文档路由
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 应用路由
    path('music/', include('music.urls')),
    path('user/', include('users.urls')),
    path('playlist/', include('playlist.urls')),

    # 认证系统
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', Login.as_view(), name='custom_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 原始 API 描述文件
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

# 开发模式下启用媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)