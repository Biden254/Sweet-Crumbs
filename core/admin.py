from django.contrib import admin
from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("updated_at", "llm_enabled")
    list_editable = ("llm_enabled",)

# Register your models here.
