from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Application, Department, ApplicationDepartment, UserApplication
from .serializers import UserSerializer, ApplicationSerializer, ShortApplicationSerializer, DepartmentSerializer, \
    ApplicationPropertySerializer, UserApplicationSerializer, ClassicApplicationSerializer
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
        raise ValidationError({"message": f'Incorrect Login credentials'})
    if user:
        if user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
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


class ShortApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ShortApplicationSerializer
    permission_classes = [IsAuthenticated]


class DepartmentListView(ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.all().order_by('name')


class UserApplicationsListListView(ListAPIView):
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
                is_active=1, for_student=1, pk__in=application_ids)
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


class UserApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            "user": request.user.pk,
            "application": self.kwargs["id"]
        }
        serializer = UserApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_user_application_property(
                serializer.data['id'], dict(request.POST))
            a = Application.objects.get(pk=serializer.data['application'])
            d = DocFormatter(a)
            d.save_new_document(serializer.data['id'], dict(request.POST))

            return Response({"data": serializer.data}, status=200)
        else:
            return Response({"message": serializer.errors}, status=400)


class ApplicationView(APIView):

    def get_object(self, pk):
        return Application.objects.get(pk=pk)

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
        return Response({"message": 'Successful delete'}, status=200)


class ApplicationPropertyListView(ListAPIView):
    serializer_class = ApplicationPropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.data.get('id', None)
        application = Application.objects.get(pk=id)
        applications = Application.objects.filter(application=application)

        return applications
