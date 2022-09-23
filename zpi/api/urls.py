from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers

from .views import YourView

router = routers.SimpleRouter()
# router.register(r'test', YourView)

urlpatterns = [
    # path('api/', include(router.urls)),
    path('api/', YourView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]