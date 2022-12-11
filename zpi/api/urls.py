from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.models import User
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from .views import user_login, user_logout, change_password, download_file, ShortApplicationListView, \
    ApplicationListView, ApplicationView, DepartmentListView, ApplicationPropertyListView, \
    UserApplicationView, UserApplicationsListView, UserApplicationPropertyListView, UserApplicationStatusUpdateView, \
    UserApplicationsToCheckListView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls, name='admin'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('file/download/', download_file, name='download_file'),
    path('change_password/', change_password, name='change_password'),

    path('basic/applications/', ShortApplicationListView.as_view(),
         name="get_applications"),
    path('basic/departments/', DepartmentListView.as_view(), name="get_departments"),

    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('application/<int:id>/', ApplicationView.as_view(), name='application'),
    path('application/<int:id>/properties/',
         ApplicationPropertyListView.as_view(), name='application-properties'),

    path('user/applications/', UserApplicationsListView.as_view(),
         name="user_applications"),
    path('user/applications/to/check/', UserApplicationsToCheckListView.as_view(),
         name="user_applications_to_check"),
    path('user/application/<int:id>/',
         UserApplicationView.as_view(), name='user-application'),
    path('user/application/<int:id>/status/update/',
         UserApplicationStatusUpdateView.as_view(), name='user-application'),
    path('user/application/<int:id>/properties/',
         UserApplicationPropertyListView.as_view(), name='user-application-properties'),



]
