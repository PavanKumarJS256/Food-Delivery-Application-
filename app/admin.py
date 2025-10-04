from django.contrib import admin

from app.models import Foods, Order, Restaurants

# Register your models here
admin.site.register(Restaurants)
admin.site.register(Foods)
admin.site.register(Order)