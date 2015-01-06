from django.contrib import admin

from .models import Shift, UserAccount

admin.site.register(Shift)
admin.site.register(UserAccount)