from rest_framework import views
from rest_framework.response import Response

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
