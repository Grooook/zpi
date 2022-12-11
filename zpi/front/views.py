import requests
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib import messages

from .utils import generate_request_headers
from .forms import ApplicationForm, UserApplicationForm


def handler404(request, *args, **kwargs):
    return HttpResponseRedirect('/')


def main_page(request):
    response = requests.get('http://localhost:8000/api/basic/applications/',
                            headers=generate_request_headers(request)).json()
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
            return redirect('front:main')
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
    return redirect('front:login')


class ApplicationListView(View):
    def get(self, request):
        applications = requests.get('http://localhost:8000/api/applications/', data=dict(request.GET),
                                    headers=generate_request_headers(request))
        departments = requests.get('http://localhost:8000/api/basic/departments/',
                                   headers=generate_request_headers(request))
        return render(request, 'applications.html', {'applications': applications.json(), 'departments': departments.json()})


class ApplicationToCheckListView(View):
    def get(self, request):
        applications = requests.get('http://localhost:8000/api/user/applications/to/check/', data=dict(request.GET),
                                    headers=generate_request_headers(request))
        return render(request, 'applications_to_check.html', {'applications': applications.json()})


class UserApplicationListView(View):
    def get(self, request):
        name = request.GET.get('name', None)
        is_active = request.GET.get('is_active', None)
        get_data = {
            'name': name,
            'is_active': is_active,
        }
        response = requests.get('http://localhost:8000/api/user/applications/', data=get_data,
                                headers=generate_request_headers(request))

        return render(request, 'user_applications.html', {'applications': response.json()})


class ApplicationCreateView(View):
    def get(self, request):
        response = requests.get('http://localhost:8000/api/basic/departments/',
                                headers=generate_request_headers(request))
        form = ApplicationForm(departments=response.json())
        context = {'submit': 'Add application', 'form': form}

        return render(request, 'application_form.html', context)

    def post(self, request):
        response = requests.post('http://localhost:8000/api/applications/', data=dict(request.POST), files=request.FILES,
                                 headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:applications')
        messages.error(request, response.json())

        return redirect('front:create_new_application')


class UserApplicationCreateView(View):
    def get(self, request, id):
        context = {}
        response = requests.get(f'http://localhost:8000/api/application/{id}/properties/',
                                headers=generate_request_headers(request))
        if response.status_code == 404:
            return redirect('front:user_applications')
        context['application'] = {property['name']: property['required'] for property in response.json()}
        form = UserApplicationForm(data=context['application'], user_data=request.session['user'])
        context = {'submit': 'Add application', 'form': form}

        return render(request, 'user_application_form.html', context)

    def post(self, request, id):
        response = requests.post(f'http://localhost:8000/api/user/application/{id}/', data=dict(request.POST), files=request.FILES,
                                 headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:user_applications')
        messages.error(request, response.json())

        return redirect('front:create_user_application', id=id)


class ApplicationUpdateView(View):
    def get(self, request, *args, **kwargs):
        context = {'method': 'PUT', 'submit': 'Update application'}
        response = requests.get(f'http://localhost:8000/api/application/{self.kwargs["id"]}/',
                                headers=generate_request_headers(request))

        if response.status_code == 404:
            return redirect('front:applications')
        context['application'] = response.json()
        response = requests.get('http://localhost:8000/api/basic/departments/',
                                headers=generate_request_headers(request))
        context['form'] = ApplicationForm(
            departments=response.json(), initial=context['application']['data'])

        return render(request, 'application_form.html', context)

    def post(self, request, *args, **kwargs):
        response = requests.patch(f'http://localhost:8000/api/application/{self.kwargs["id"]}/', data=dict(request.POST),
                                  headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:applications')
        messages.error(request, response.json())

        return redirect('front:update_application', id=self.kwargs["id"])


class ApplicationDeleteView(View):
    def get(self, request, *args, **kwargs):
        response = requests.delete(f'http://localhost:8000/api/application/{self.kwargs["id"]}/',
                                   headers=generate_request_headers(request))

        return redirect('front:applications')


class UserApplicationUpdateView(View):
    def get(self, request, id):
        context = {'method': 'PUT', 'submit': 'Update application'}
        response = requests.get(f'http://localhost:8000/api/user/application/{id}/properties/',
                                headers=generate_request_headers(request))

        if response.status_code == 404:
            return redirect('front:user_applications')
        context['application'] = {property['name']: property['value'] for property in response.json()}
        response = requests.get(f'http://localhost:8000/api/application/{id}/properties/',
                                headers=generate_request_headers(request))
        if response.status_code == 404:
            return redirect('front:user_applications')
        context['data'] = {property['name']: property['required'] for property in response.json()}
        context['form'] = UserApplicationForm(data=context['data'], user_data=request.session['user'], initial=context['application'])

        return render(request, 'user_application_form.html', context)

    def post(self, request, id):
        response = requests.patch(f'http://localhost:8000/api/user/application/{id}/', data=dict(request.POST),
                                  headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:user_applications')
        messages.error(request, response.json())

        return redirect('front:update_user_application', id=id)


class UserApplicationStatusUpdateView(View):
    def get(self, request, id):
        response = requests.patch(f'http://localhost:8000/api/user/application/{id}/status/update/', data=dict(request.GET),
                                  headers=generate_request_headers(request))
        if response.status_code != 200:
            messages.error(request, response.json())

        return redirect(request.META.get('HTTP_REFERER'))


class UserApplicationDeleteView(View):
    def get(self, request, *args, **kwargs):
        response = requests.delete(f'http://localhost:8000/api/user/application/{self.kwargs["id"]}/',
                                   headers=generate_request_headers(request))
        if response.status_code == 200:
            messages.success(request, response.json())
        else:
            messages.error(request, response.json())

        return redirect('front:user_applications')
