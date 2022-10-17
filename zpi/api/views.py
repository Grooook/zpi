from django.http import JsonResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import YourSerializer


class LoginView(views.APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request):
        index = request.data.get('index')
        password = request.data.get('password')
        if (index == 'test' and password == 'test'):
            result = {'status': "ok", 'message': "You are successfully login",
                      "accessToken": "accessToken", "user": []}
        else:
            result = {'status': "fail", 'message': "Student ID or password s incorrect"}
        return Response(result)

@api_view(['GET'])
def get_applications(request):
    search_help = ['Wniosek 1', 'Wniosek 2', 'Wniosek 3']
    return Response(search_help)


@api_view(['GET'])
def get_user_applications(request):
    
    return Response()