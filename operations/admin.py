from django.contrib import admin
from operations import models


admin.site.register(models.Account)
admin.site.register(models.Operation)
