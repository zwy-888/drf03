from django.contrib import admin

# Register your models here.
# 将当前模型注册到后台站点使用
from api import models

admin.site.register(models.Employee)
