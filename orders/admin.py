from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.OrderModel)
admin.site.register(models.OrderItemModel)
