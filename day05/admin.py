from django.contrib import admin

# Register your models here.
from day05 import models

admin.site.register(models.Employee2)
admin.site.register(models.Dept)