from email.mime import application
from turtle import position
import uuid
from django.db import models

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
    

class PropertyType(models.Model):
    name = models.CharField(max_length=127)
    propery_type = models.CharField(max_length=127)
    max_length = models.PositiveSmallIntegerField()
    

class ApplicationProperty(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    property = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    value = models.CharField(max_length=127)
    url = models.URLField(blank=True, null=True)
    

class UserApplication(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    
    
class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=32)