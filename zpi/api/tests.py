import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .models import User, Department
from .serializers import DepartmentSerializer
from rest_framework.test import APIClient

client = APIClient()
user = User.objects.get(email='248795@example.com')
token, _ = Token.objects.get_or_create(user=user)
client.force_authenticate(user=user)


class GetAllDepartments(TestCase):
    def setUp(self):
        pass

    def test_get_all_departments(self):
        response = client.get(reverse('get_departments'))
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



