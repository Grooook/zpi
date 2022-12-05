from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.get_object_or_none(username=username)
    if not user:
        user = User.objects.get_object_or_none(email=username)
    print(check_password(password, user.password), user.password)
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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_applications(request):
    search_help = ['Wniosek 1', 'Wniosek 2', 'Wniosek 3']
    return Response(search_help)


@api_view(['GET'])
def get_user_applications(request):
    return Response()
