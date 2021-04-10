"""myDjangoRestful URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework import permissions

# swagger
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

from myDjangoRestful.api.user import UserLoginApi, UserRegisterApi, UserApi
from myDjangoRestful.api.chart import ChartApi
from myDjangoRestful.api.datasource import DatasourceApiView, DatasourceDetailApiView


schema_view = get_schema_view(
    openapi.Info(
        title="Chart API",
        default_version='v1',
        description="Hello World",
        terms_of_service="https://127.0.0.1:8000",
        contact=openapi.Contact(email="1342468180@qq.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 注册restfulApi
router = routers.DefaultRouter()
router.register(r'charts', ChartApi)
# router.register(r'datasources', DatasourceApi)

urlpatterns = [
    path('admin/', admin.site.urls),

    # swagger文档
    re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- 这里
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  #<-- 这里
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  #<-- 这里

    url(r'^', include(router.urls)),

    url(r'^users/$', UserApi.as_view()),
    url(r'^users/login/$', UserLoginApi.as_view()),
    url(r'^users/register/$', UserRegisterApi.as_view()),

    url(r'^datasources/$', DatasourceApiView.as_view()),
    url(r'^datasources/(?P<hash_id>[a-z|0-9]+)/$', DatasourceDetailApiView.as_view()),
]