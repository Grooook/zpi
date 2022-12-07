from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import main_page, login, logout, ApplicationListView, ApplicationCreateView, ApplicationUpdateView, ApplicationDeleteView

app_name = 'front'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', main_page, name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('applications/', ApplicationListView.as_view(), name='applications'),
    path('create_application/', ApplicationCreateView.as_view(), name='create_application'),
    path('update_application/<int:id>/', ApplicationUpdateView.as_view(), name='update_application'),
    path('delete_application/<int:id>/', ApplicationDeleteView.as_view(), name='delete_application'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'front.views.handler404'
