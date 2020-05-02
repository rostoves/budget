from django.contrib import admin
from categories import models


admin.site.register(models.Type)
admin.site.register(models.Category)
admin.site.register(models.MerchantCode)
admin.site.register(models.Description)
admin.site.register(models.Currency)

