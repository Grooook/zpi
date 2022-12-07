from django.shortcuts import get_object_or_404

from api.models import Application
from api.serializers import ApplicationDepartmentSerializer


def get_application_from_kwargs(kwargs):
    pk = kwargs['id']
    application = get_object_or_404(Application, pk=pk)

    return application


def create_application_department(application, departments):
    for department in departments:
        data = {
            'application': application,
            'department': department
        }
        application_department = ApplicationDepartmentSerializer(data=data)
        if application_department.is_valid():
            application_department.save()



