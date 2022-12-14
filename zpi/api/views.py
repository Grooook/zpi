import os

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _

from .models import User, Application, Department, ApplicationDepartment, UserApplication, ApplicationProperty, \
    Property, UserApplicationProperty, ApplicationHistory
from .serializers import UserSerializer, ApplicationSerializer, ShortApplicationSerializer, DepartmentSerializer, \
    ApplicationPropertySerializer, UserApplicationSerializer, ClassicApplicationSerializer, PropertySerializer, \
    UserApplicationPropertySerializer
from .utils.utils import create_application_department, create_user_application_property, get_application_post_data
from .utils.docFormatter import DocFormatter


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.get_object_or_none(username=username)
    if not user:
        user = User.objects.get_object_or_none(email=username)
    if not user or not check_password(password, user.password):
        raise ValidationError({"message": _('Incorrect Login credentials')})
    if user:
        if user.is_active:
            token, a = Token.objects.get_or_create(user=user)
            user_serialized = UserSerializer(user)
            response = {"user": user_serialized.data, "token": token.key}
            return Response(response)
        else:
            raise ValidationError({"message": f'Account not active'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response('User Logged out successfully')


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    user = request.data.get('user')
    password = request.data.get('password')
    user = User.objects.get_object_or_none(pk=user)
    user.set_password(password)
    user.save()
    return Response('User passsword has changed')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request):
    file = request.GET.get('file', None)
    file = file.replace('http://localhost:8000/', '')
    if os.path.exists(file):
        with open(file, 'rb') as document:
            content = document.read()
            response = HttpResponse(
                content,
                content_type='application/msword'
            )
            file_name = file.split('/')[-1]
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            response['Content-Length'] = len(content)
            return response
    else:
        return Response('File not found', status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_pdf_file(request):
    file = request.GET.get('file', None)
    file = file.replace('http://localhost:8000/', '')
    if os.path.exists(file):
        with open(file, 'rb') as document:
            content = document.read()
            response = HttpResponse(
                content,
                content_type='application/msword'
            )
            file_name = file.split('/')[-1]
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            response['Content-Length'] = len(content)
            return response
    else:
        return Response('File not found', status=404)


class ShortApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ShortApplicationSerializer
    permission_classes = [IsAuthenticated]


class DepartmentListView(ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.all().order_by('name')


class UserApplicationsListView(ListAPIView):
    serializer_class = UserApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_applications = UserApplication.objects.filter(
            user=user).order_by('-submission_date')
        name = self.request.data.get('name', None)
        if name:
            user_applications = user_applications.filter(
                application__name__contains=name)

        return user_applications


class UserApplicationsToCheckListView(ListAPIView):
    serializer_class = UserApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_applications = UserApplication.objects.filter(
            application__accepted_by__in=user.can_check_permissions(), status='p').order_by('-submission_date')
        name = self.request.data.get('name', None)
        if name:
            user_applications = user_applications.filter(
                application__name__contains=name)

        return user_applications


class ApplicationListView(ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        applications = Application.objects.all().order_by('name')
        user = self.request.user

        name = self.request.data.get('name', None)
        is_active = self.request.data.get('is_active', None)
        department = self.request.data.get('department', None)
        if name:
            applications = applications.filter(name__contains=name)
        if user.is_student:
            application_ids = ApplicationDepartment.objects.filter(
                department=user.department).values_list('application')
            applications = applications.filter(
                is_active=1, pk__in=application_ids)
        elif is_active:
            applications = applications.filter(is_active=is_active)
        if user.is_staff and department:
            department = Department.objects.get(short_name=department)
            application_ids = ApplicationDepartment.objects.filter(
                department=department.pk).values_list('application')
            applications = applications.filter(pk__in=application_ids)

        return applications

    def create(self, request, *args, **kwargs):
        user = request.user
        file = request.FILES['file']
        post_data = get_application_post_data(request, user.pk, file)

        serializer = ApplicationSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            create_application_department(
                serializer.data['id'], dict(request.POST)['departments'])
            a = Application.objects.get(pk=serializer.data['id'])
            d = DocFormatter(a)
            d.save_to_db()

            return Response({"data": serializer.data}, status=200)
        else:
            return Response({"message": serializer.errors}, status=400)


class ApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Application, pk=pk)

    def get(self, request, id):
        application = self.get_object(id)
        serializer = ApplicationSerializer(application)
        return Response({"data": serializer.data}, status=200)

    def patch(self, request, id):
        request_data = dict(request.POST)
        post_data = get_application_post_data(request)

        application = self.get_object(id)
        serializer = ApplicationSerializer(
            application, data=post_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ApplicationDepartment.objects.filter(application=id).delete()
            create_application_department(id, request_data['departments'])
            return Response(data=serializer.data)
        return Response({'message': "Wrong parameters"}, status=400)

    def delete(self, request, id):
        application = self.get_object(id)
        application.delete()
        return Response({"message": 'Successfully deleted'}, status=200)


class UserApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(UserApplication,pk=pk)

    def get(self, request, id):
        application = self.get_object(id)
        serializer = UserApplicationSerializer(application)

        return Response({"data": serializer.data}, status=200)

    def post(self, request, id):
        data = {
            "user": request.user.pk,
            "application": id
        }
        serializer = UserApplicationSerializer(data=data)
        if serializer.is_valid():
            request_data = dict(request.POST)
            properties = Property.objects.all()
            for property in properties:
                if property.name in request_data and len(request_data[property.name][0]) > property.max_length:
                    return Response({"message": property.name + ' ' + \
                                                _('must have max length: ') + str(property.max_length)}, status=400)
            serializer.save()
            create_user_application_property(
                serializer.data['id'], dict(request.POST))
            application = Application.objects.get(pk=serializer.data['application'])
            document = DocFormatter(application)
            document.save_new_document(serializer.data['id'], dict(request.POST))
            return Response({"data": serializer.data}, status=200)
        else:
            return Response({"message": serializer.errors}, status=400)

    def patch(self, request, id):
        request_data = dict(request.POST)
        properties = Property.objects.all()
        for property in properties:
            if property.name in request_data and len(request_data[property.name][0]) > property.max_length:
                return Response({"message": property.name + ' ' + \
                                    _('must have max length: ') + str(property.max_length)}, status=400)
        if 'csrfmiddlewaretoken' in request_data:
            del request_data['csrfmiddlewaretoken']
        application_id = None
        for key, value in request_data.items():
            user_application = UserApplicationProperty.objects.filter(user_application__pk=id, property__name=key).first()
            application_id = user_application.user_application.application.pk
            user_application.value = value[0]
            user_application.save()
        document = DocFormatter(Application.objects.get(pk=application_id))
        document.update_document(id)
        return Response({'message': "Successfully updated"}, status=200)

    def delete(self, request, id):
        user_application = self.get_object(id)
        user_application.delete()
        return Response({"message": 'Successfully deleted'}, status=200)


class UserApplicationStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        new_status = request.data.get('status', None)
        user = request.user
        if not new_status:
            return Response({"message": "No status passed"}, status=400)
        user_application = get_object_or_404(UserApplication, pk=id)
        if (user_application.status == 'c' and new_status in ['p']) \
                or (user_application.status == 'p' and new_status in ['a', 'r', 'd']):
            history = ApplicationHistory()
            history.user = user
            history.user_application = user_application
            history.status = user_application.status
            history.new_status = new_status
            history.save()

            user_application.status = new_status
            user_application.save()
            return Response({"message": 'Successfully updated'}, status=200)

        return Response({"message": 'Not available to change'}, status=400)


class ApplicationPropertyListView(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['id']
        application_properties = ApplicationProperty.objects.filter(application__id=id).values_list('property', flat=True)
        properties = Property.objects.filter(pk__in=list(application_properties))
        return properties


class UserApplicationPropertyListView(ListAPIView):
    serializer_class = UserApplicationPropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['id']
        user_application_properties = UserApplicationProperty.objects.filter(user_application__id=id)
        return user_application_properties
