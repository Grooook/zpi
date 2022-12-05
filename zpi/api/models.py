import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, name, surname, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, surname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
            password=password,
        )
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
    birth_date = models.CharField(max_length=30, blank=True, null=True, default=None)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    is_super_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser


class Application(models.Model):
    name = models.CharField(max_length=127)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey('Application', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='documents/')


class FieldType(models.Model):
    field_types = [
        ("", "Date"),
        ("", "DateTime"),
        ("", "Time"),
        ("", "Decimal"),
        ("", "Char"),
        ("", "Intager"),
        ("", ""),
    ]
    name = models.CharField(max_length=127, choices=field_types)


class Property(models.Model):
    name = models.CharField(max_length=127)
    property_type = models.CharField(max_length=127)
    max_length = models.PositiveSmallIntegerField()


class UserApplication(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)


class UserApplicationProperty(models.Model):
    user_application = models.ForeignKey(UserApplication, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    value = models.TextField(max_length=1024)
    url = models.URLField(blank=True, null=True)
    editable = models.BooleanField(default=False)
    font = models.CharField(max_length=125, default="Arial")
    font_size = models.PositiveSmallIntegerField(default=12, validators=[MaxValueValidator(72)])
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    is_underline = models.BooleanField(default=False)


class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=32)
