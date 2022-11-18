from django.urls import path, include
from django.views.generic import TemplateView

from .views import main_page

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', main_page, name='main'),
]