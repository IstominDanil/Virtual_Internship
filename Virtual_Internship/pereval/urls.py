from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework import routers
from .views import PassageViewSet

router = routers.DefaultRouter()
router.register(r'submitData', PassageViewSet, basename='passage')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)