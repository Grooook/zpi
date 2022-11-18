from django.shortcuts import render
from django.views import View
import requests
from django.views.i18n import set_language

def main_page(request):
    response = requests.get('http://localhost:8000/api/get_applications/')
    return render(request, 'main.html', {'context': response.json()})

class LoginView(View):
    pass
