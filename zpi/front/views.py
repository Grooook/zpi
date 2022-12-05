import requests
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render

from .utils import generate_request_headers


def handler404(request, *args, **kwargs):
    return HttpResponseRedirect('/')


def main_page(request):
    response = requests.get('http://localhost:8000/api/get_applications/').json()
    return render(request, 'main.html', {'context': response})


def login(request):
    context = None
    if request.method == 'POST':
        post_data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        response = requests.post('http://localhost:8000/api/login/', post_data)
        if response.status_code == 200:
            request.session['is_authenticated'] = True
            request.session['auth_token'] = response.json()['token']
            request.session['user'] = response.json()['user']
            return redirect('main')
        context = {'message': response.json()['message']}

    return render(request, 'login.html', context)


def logout(request):
    response = requests.post(
        'http://localhost:8000/api/logout/',
        headers=generate_request_headers(request)
    )
    if response.status_code == 200 and request.session['is_authenticated']:
        del request.session['is_authenticated']
        del request.session['auth_token']
        del request.session['user']
    return redirect('main')



