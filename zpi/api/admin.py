from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Application)
admin.site.register(Property)
admin.site.register(UserApplication)
admin.site.register(UserApplicationProperty)
admin.site.register(ApplicationHistory)

