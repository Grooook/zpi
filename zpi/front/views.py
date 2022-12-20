import requests
import urllib.request
import io
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _

from .decorators import authenticated_user
from .utils import generate_request_headers
from .forms import ApplicationForm, UserApplicationForm


def handler404(request, *args, **kwargs):
    return HttpResponseRedirect('/')


@authenticated_user
def main_page(request):
    response = requests.get(settings.BASE_URL + 'api/basic/applications/',
                            headers=generate_request_headers(request)).json()
    return render(request, 'main.html', {'context': response})


def login(request):
    context = None
    if request.method == 'POST':
        post_data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        response = requests.post(settings.BASE_URL + 'api/login/', post_data)
        if response.status_code == 200:
            request.session['is_authenticated'] = True
            request.session['auth_token'] = response.json()['token']
            request.session['user'] = response.json()['user']
            return redirect('front:main')
        context = {'message': response.json()['message']}

    return render(request, 'login.html', context)


@authenticated_user
def logout(request):
    response = requests.post(
        settings.BASE_URL + 'api/logout/',
        headers=generate_request_headers(request)
    )
    if response.status_code == 200 and request.session['is_authenticated']:
        del request.session['is_authenticated']
        del request.session['auth_token']
        del request.session['user']
    return redirect('front:login')


@authenticated_user
def open_pdf(request):
    r = requests.get(request.GET['file'])
    # print(r.content)
    with io.BytesIO(r.content) as inmemoryfile:
        print(inmemoryfile)
    return redirect('front:applications_to_check')


class ApplicationListView(View):
    def get(self, request):
        applications = requests.get(settings.BASE_URL + 'api/applications/', data=dict(request.GET),
                                    headers=generate_request_headers(request))
        departments = requests.get(settings.BASE_URL + 'api/basic/departments/',
                                   headers=generate_request_headers(request))
        if applications.status_code == 401 or departments.status_code == 401:
            return redirect('front:login')
        return render(request, 'applications.html', {'applications': applications.json(), 'departments': departments.json()})


class ApplicationToCheckListView(View):
    def get(self, request):
        applications = requests.get(settings.BASE_URL + 'api/user/applications/to/check/', data=dict(request.GET),
                                    headers=generate_request_headers(request))
        if applications.status_code == 401:
            return redirect('front:login')
        return render(request, 'applications_to_check.html', {'applications': applications.json()})


class UserApplicationListView(View):
    def get(self, request):
        name = request.GET.get('name', None)
        is_active = request.GET.get('is_active', None)
        get_data = {
            'name': name,
            'is_active': is_active,
        }
        response = requests.get(settings.BASE_URL + 'api/user/applications/', data=get_data,
                                headers=generate_request_headers(request))
        if response.status_code == 401:
            return redirect('front:login')
        return render(request, 'user_applications.html', {'applications': response.json()})


class ApplicationCreateView(View):
    def get(self, request):
        response = requests.get(settings.BASE_URL + 'api/basic/departments/',
                                headers=generate_request_headers(request))
        if response.status_code == 401:
            return redirect('front:login')
        form = ApplicationForm(departments=response.json())
        context = {'submit': _('Add application'), 'form': form}

        return render(request, 'application_form.html', context)

    def post(self, request):
        response = requests.post(settings.BASE_URL + 'api/applications/', data=dict(request.POST), files=request.FILES,
                                 headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:applications')
        elif response.status_code == 401:
            return redirect('front:login')
        messages.error(request, response.json())

        return redirect('front:create_new_application')


class UserApplicationCreateView(View):
    def get(self, request, id):
        context = {}
        response = requests.get(settings.BASE_URL + f'api/application/{id}/properties/',
                                headers=generate_request_headers(request))
        if response.status_code == 404:
            messages.error(request, response.json())
            return redirect('front:user_applications')
        elif response.status_code == 401:
            return redirect('front:login')
        elif response.status_code == 400:
            messages.error(request, response.json())
            return redirect('front:create_user_application')
        properties = {property['name']: {'required': property['required'], 'max_length': property['max_length']} \
                      for property in response.json()}
        form = UserApplicationForm(data=properties, user_data=request.session['user'])
        context = {'submit': _('Add application'), 'form': form}

        return render(request, 'user_application_form.html', context)

    def post(self, request, id):
        response = requests.post(settings.BASE_URL + f'api/user/application/{id}/', data=dict(request.POST), files=request.FILES,
                                 headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:user_applications')
        elif response.status_code == 401:
            return redirect('front:login')
        messages.error(request, response.json())

        return redirect('front:create_user_application', id=id)


class ApplicationUpdateView(View):
    def get(self, request, *args, **kwargs):
        context = {'method': 'PUT', 'submit': 'Update application'}
        response = requests.get(settings.BASE_URL + f'api/application/{self.kwargs["id"]}/',
                                headers=generate_request_headers(request))

        if response.status_code == 404:
            return redirect('front:applications')
        elif response.status_code == 401:
            return redirect('front:login')
        context['application'] = response.json()
        response = requests.get(settings.BASE_URL + 'api/basic/departments/',
                                headers=generate_request_headers(request))
        context['form'] = ApplicationForm(
            departments=response.json(), initial=context['application']['data'])

        return render(request, 'application_form.html', context)

    def post(self, request, *args, **kwargs):
        response = requests.patch(settings.BASE_URL + f'api/application/{self.kwargs["id"]}/', data=dict(request.POST),
                                  headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:applications')
        elif response.status_code == 401:
            return redirect('front:login')
        messages.error(request, response.json())

        return redirect('front:update_application', id=self.kwargs["id"])


class ApplicationDeleteView(View):
    def get(self, request, *args, **kwargs):
        response = requests.delete(settings.BASE_URL + f'api/application/{self.kwargs["id"]}/',
                                   headers=generate_request_headers(request))
        if response.status_code == 401:
            return redirect('front:login')
        return redirect('front:applications')


class UserApplicationUpdateView(View):
    def get(self, request, id):
        context = {'method': 'PUT', 'submit': 'Update application'}
        response = requests.get(settings.BASE_URL + f'api/user/application/{id}/properties/',
                                headers=generate_request_headers(request))

        if response.status_code == 404:
            return redirect('front:user_applications')
        if response.status_code == 401:
            return redirect('front:login')
        response_data = response.json()
        context['application'] = {property['name']: property['value'] for property in response_data}
        response = requests.get(settings.BASE_URL + f'api/application/{response_data[0]["application"]}/properties/',
                                headers=generate_request_headers(request))
        if response.status_code == 404:
            return redirect('front:user_applications')
        properties = {property['name']: {'required': property['required'], 'max_length': property['max_length']} \
                      for property in response.json()}
        context['form'] = UserApplicationForm(data=properties, user_data=request.session['user'], initial=context['application'])

        return render(request, 'user_application_form.html', context)

    def post(self, request, id):
        response = requests.patch(settings.BASE_URL + f'api/user/application/{id}/', data=dict(request.POST),
                                  headers=generate_request_headers(request))
        if response.status_code == 200:
            return redirect('front:user_applications')
        elif response.status_code == 401:
            return redirect('front:login')
        messages.error(request, response.json())

        return redirect('front:update_user_application', id=id)


class UserApplicationStatusUpdateView(View):
    def get(self, request, id):
        response = requests.patch(settings.BASE_URL + f'api/user/application/{id}/status/update/', data=dict(request.GET),
                                  headers=generate_request_headers(request))
        if response.status_code == 401:
            return redirect('front:login')
        elif response.status_code != 200:
            messages.error(request, response.json())

        return redirect(request.META.get('HTTP_REFERER'))


class UserApplicationDeleteView(View):
    def get(self, request, *args, **kwargs):
        response = requests.delete(settings.BASE_URL + f'api/user/application/{self.kwargs["id"]}/',
                                   headers=generate_request_headers(request))
        if response.status_code == 200:
            messages.success(request, response.json())
        elif response.status_code == 401:
            return redirect('front:login')
        else:
            messages.error(request, response.json())

        return redirect('front:user_applications')
