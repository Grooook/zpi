from django.shortcuts import get_object_or_404

from api.models import Application, Property
from api.serializers import ApplicationDepartmentSerializer

from api.serializers import UserApplicationPropertySerializer


def get_application_from_kwargs(kwargs):
    pk = kwargs['id']
    application = get_object_or_404(Application, pk=pk)

    return application


def get_property_dict():
    properties = Property.objects.all().values('name', 'pk')
    properties = {property['name']: property['pk'] for property in properties}

    return properties


def create_application_department(application, departments):
    for department in departments:
        data = {
            'application': application,
            'department': department
        }
        application_department = ApplicationDepartmentSerializer(data=data)
        if application_department.is_valid():
            application_department.save()


def create_user_application_property(user_application, properties):
    db_properties = get_property_dict()
    if 'csrfmiddlewaretoken' in properties:
        del properties['csrfmiddlewaretoken']
    for property in properties.keys():
        data = {
            'user_application': user_application,
            'property': db_properties[property],
            'position': 0,
            'value': properties[property][0]
        }
        user_application_property = UserApplicationPropertySerializer(data=data)
        if user_application_property.is_valid():
            user_application_property.save()


def get_application_post_data(request, user=None, file=None):
    request_data = dict(request.POST)
    post_data = request.POST.copy()
    post_data._mutable = True
    if user: post_data['creator'] = user
    if file: post_data['file'] = file
    post_data['is_active'] = False if 'is_active' not in request_data else post_data['is_active']

    return post_data
