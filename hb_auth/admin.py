from django.contrib import admin
from .models import ClientDetail, HbApplications


# Register your models here.

@admin.register(ClientDetail)
class ClientDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'reqCount', 'apiKey', 'createdAt', 'isActive')
    readonly_fields = ('apiKey',)


@admin.register(HbApplications)
class HbApplicationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'createdAt')
