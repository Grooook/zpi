from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import main_page, login, logout, ApplicationListView, ApplicationCreateView, ApplicationUpdateView, \
    ApplicationDeleteView, UserApplicationCreateView, UserApplicationListView, UserApplicationDeleteView, UserApplicationUpdateView

app_name = 'front'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', main_page, name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('create_new_application/', ApplicationCreateView.as_view(),
         name='create_new_application'),

    path('applications/', ApplicationListView.as_view(), name='applications'),
    path('update/application/<int:id>/',
         ApplicationUpdateView.as_view(), name='update_application'),
    path('delete/application/<int:id>/',
         ApplicationDeleteView.as_view(), name='delete_application'),

    path('user_applications/', UserApplicationListView.as_view(),
         name='user_applications'),
    path('create/user/application/<int:id>/',
         UserApplicationCreateView.as_view(), name='create_user_application'),
    path('delete/user/application/<int:id>/',
         UserApplicationDeleteView.as_view(), name='delete_user_application'),
    path('update/user/application/<int:id>/',
         UserApplicationUpdateView.as_view(), name='update_user_application'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'front.views.handler404'
