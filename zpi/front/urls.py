from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import main_page, login, logout, ApplicationListView, ApplicationCreateView, ApplicationUpdateView, \
    ApplicationDeleteView, UserApplicationCreateView, UserApplicationListView, UserApplicationDeleteView, \
    UserApplicationUpdateView, UserApplicationStatusUpdateView, ApplicationToCheckListView, open_pdf

app_name = 'front'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', main_page, name='main'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('file/', open_pdf, name='open_pdf'),

    path('create/new/application/', ApplicationCreateView.as_view(),
         name='create_new_application'),

    path('applications/', ApplicationListView.as_view(), name='applications'),
    path('applications/to/check/',
         ApplicationToCheckListView.as_view(), name='applications_to_check'),

    path('application/<int:id>/update/',
         ApplicationUpdateView.as_view(), name='update_application'),
    path('application/<int:id>/delete/',
         ApplicationDeleteView.as_view(), name='delete_application'),

    path('user/applications/', UserApplicationListView.as_view(),
         name='user_applications'),
    path('user/application/<int:id>/create/',
         UserApplicationCreateView.as_view(), name='create_user_application'),
    path('user/application/<int:id>/delete/',
         UserApplicationDeleteView.as_view(), name='delete_user_application'),
    path('user/application/<int:id>/update/',
         UserApplicationUpdateView.as_view(), name='update_user_application'),
    path('user/application/status/<int:id>/update/',
         UserApplicationStatusUpdateView.as_view(), name='change_user_application_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'front.views.handler404'
