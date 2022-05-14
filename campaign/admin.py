from django.contrib import admin
from campaign.models import Domain, EmailTemplate

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)