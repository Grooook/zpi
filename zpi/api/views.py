from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Application, Department, ApplicationDepartment
from .serializers import UserSerializer, ApplicationSerializer, ShortApplicationSerializer, DepartmentSerializer
from .utils.utils import create_application_department
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


@api_view(['GET'])
def get_user_applications(request):
    return Response()


class ApplicationListView(ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        applications = Application.objects.all().order_by('name')
        name = self.request.data.get('name', None)
        is_active = self.request.data.get('is_active', None)
        if name:
            applications = applications.filter(name__contains=name)
        if is_active:
            applications = applications.filter(is_active=is_active)
        return applications

    def create(self, request, *args, **kwargs):
        user = request.user
        file = request.FILES['file']
        post_data = request.POST.copy()
        post_data._mutable = True
        post_data['creator'] = user.pk
        post_data['file'] = file
        serializer = ApplicationSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            create_application_department(serializer.data['id'], dict(request.POST)['departments'])
            DocFormatter(file)

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
        application = self.get_object(id)
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ApplicationDepartment.objects.filter(application=id).delete()
            create_application_department(id, dict(request.POST)['departments'])
            return Response(data=serializer.data)
        return Response({'message': "Wrong parameters"}, status=400)

    def delete(self, request, id):
        application = self.get_object(id)
        application.delete()
        return Response({"message": 'Successful delete'}, status=200)
