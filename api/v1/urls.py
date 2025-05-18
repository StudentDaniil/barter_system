from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.v1.views import views


app_name = 'v1'

router = routers.DefaultRouter()
router.register(r'ads', views.AdvertisementViewSet, basename='advertisement')
router.register(r'proposals', views.ExchangeProposalViewSet, basename='proposal')

schema_view = get_schema_view(
    openapi.Info(
        title="Exchange API",
        default_version='v1',
        description="API for item exchange platform",
    ),
    public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]