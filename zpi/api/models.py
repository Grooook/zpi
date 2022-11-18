import uuid
from django.db import models
from django.core.validators import MaxValueValidator

class User(models.Model):
    id = models.UUIDField(primary_key = True,
      default = uuid.uuid4, editable = False)
    last_login = models.DateTimeField(auto_now=True)


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
    