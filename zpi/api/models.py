from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, name, surname, password, department):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
            password=password,
            department=department
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, surname, password, department):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
            password=password,
            department=department,
        )
        user.is_student = True
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_dean = True
        user.is_superuser = True
        user.save(using=self._db)

    def get_object_or_none(self, *args, **kwargs):
        try:
            return User.objects.get(**kwargs)
        except:
            return None


class User(AbstractBaseUser):
    user_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    birth_date = models.CharField(
        max_length=30, blank=True, null=True, default=None)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser


class Application(models.Model):
    choices = (
        ('s', 'Staff'),
        ('t', 'Teacher'),
        ('vd', 'Vice-dean'),
        ('d', 'Dean'),
    )
    name = models.CharField(max_length=127, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    for_student = models.BooleanField(default=True)
    for_worker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    accepted_by = models.CharField(max_length=2, default='d', choices=choices)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name


class Department(models.Model):
    short_name = models.CharField(max_length=5)
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.short_name


class ApplicationDepartment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.application.name


class Property(models.Model):
    name = models.CharField(max_length=127)
    property_type = models.CharField(max_length=127)
    max_length = models.PositiveSmallIntegerField()
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ApplicationProperty(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.application.name


class UserApplication(models.Model):
    choices = (
        ('c', "Created"),
        ('p', "Pending"),
        ('a', "Accepted"),
        ('r', "Rejected"),
        ('d', "Deleted"),
    )
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=choices, default='c')
    file = models.FileField(upload_to='documents/processed/', null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            user_applications = UserApplication.objects.filter(application=self.application, user=self.user)
            for user_application in user_applications:
                if user_application.status not in ['a', 'r', 'd']:
                    raise ValidationError("User application already exists")
        super(UserApplication, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status != 'c':
            raise ValidationError("You can't delete user application")
        super(UserApplication, self).delete(*args, **kwargs)


class UserApplicationProperty(models.Model):
    user_application = models.ForeignKey(
        UserApplication, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    value = models.TextField(max_length=1024, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    editable = models.BooleanField(default=False)


class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=32)
