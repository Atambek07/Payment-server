from django.contrib import admin

from .models import Payment, Device

admin.site.register(Payment)
admin.site.register(Device)