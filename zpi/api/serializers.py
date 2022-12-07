from rest_framework import serializers

from .models import User, Application, Department, ApplicationDepartment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class ApplicationDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationDepartment
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField(method_name='get_departments')
    is_users_application = serializers.SerializerMethodField(method_name='is_application_created_by_user')

    class Meta:
        model = Application
        fields = '__all__'
        extra_fields = ('is_users_application', 'departments')

    def get_departments(self, instance):
        departments = ApplicationDepartment.objects.filter(application=instance.pk).values('department')

        return [department['department'] for department in departments]

    def is_application_created_by_user(self, instance):
        request = self.context.get('request')
        user = request.user if request else None
        if user and instance.creator.pk == user.pk:
            return True
        return False


class ShortApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('id', 'name', )


