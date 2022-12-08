from rest_framework import serializers

from .models import User, Application, Department, ApplicationDepartment, ApplicationProperty, UserApplication, \
    UserApplicationProperty


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


class ClassicApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField(
        method_name='get_departments')
    is_users_application = serializers.SerializerMethodField(
        method_name='is_application_created_by_user')
    obligatory = serializers.SerializerMethodField(
        method_name='get_obligatory')

    class Meta:
        model = Application
        fields = '__all__'
        extra_fields = ('is_users_application', 'departments', 'obligatory')

    def get_departments(self, instance):
        departments = ApplicationDepartment.objects.filter(
            application=instance.pk).values('department')

        return [department['department'] for department in departments]

    def get_obligatory(self, instance):
        obligatory_data = []
        if instance.for_student:
            obligatory_data.append('for_student')
        if instance.for_worker:
            obligatory_data.append('for_worker')
        return obligatory_data

    def is_application_created_by_user(self, instance):
        request = self.context.get('request')
        user = request.user if request else None
        if user and instance.creator.pk == user.pk:
            return True
        return False


class ApplicationPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationProperty
        fields = '__all__'


class ShortApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name',)


class UserApplicationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_application_name')
    color = serializers.SerializerMethodField(method_name='get_color')

    class Meta:
        model = UserApplication
        fields = '__all__'
        extra_fields = ('name', 'color', )

    def get_application_name(self, instance):
        application = Application.objects.get(pk=instance.application.pk)

        return application.name

    def get_color(self, instance):
        if instance.is_active and not instance.is_accepted:
            return 'info'
        elif not instance.is_active and not instance.is_accepted:
            return 'danger'

        return 'success'


class UserApplicationPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApplicationProperty
        fields = '__all__'
