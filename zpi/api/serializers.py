from rest_framework import serializers

from .models import User, Application, Department, ApplicationDepartment, ApplicationProperty, UserApplication, \
    UserApplicationProperty, Property


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

    class Meta:
        model = Application
        fields = '__all__'
        extra_fields = ('is_users_application', 'departments')

    def get_departments(self, instance):
        departments = ApplicationDepartment.objects.filter(
            application=instance.pk).values('department')

        return [department['department'] for department in departments]

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
    colored_status = serializers.SerializerMethodField(method_name='get_colored_status')

    class Meta:
        model = UserApplication
        fields = '__all__'
        extra_fields = ('name', 'colored_status', )

    def get_application_name(self, instance):
        application = Application.objects.get(pk=instance.application.pk)

        return application.name

    def get_colored_status(self, instance):
        if instance.status == 'c':
            return 'secondary'
        elif instance.status == 'p':
            return 'info'
        elif instance.status == 'a':
            return 'success'
        elif instance.status == 'r':
            return 'warning'
        else:
            return 'danger'


class UserApplicationPropertySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_application_name')

    class Meta:
        model = UserApplicationProperty
        fields = '__all__'
        extra_fields = ('name', )

    def get_application_name(self, instance):
        property = Property.objects.get(pk=instance.property.pk)

        return property.name


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
