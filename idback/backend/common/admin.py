from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

from common.models import SiteConfig, SiteSettings


class SiteConfigAdmin(SiteAdmin):
    list_display = ["domain", "name", "site_title", "support_email", "maintenance_mode"]
    fieldsets = (
        (None, {"fields": ("domain", "name")}),
        (
            "Custom fields",
            {"fields": ("site_title", "support_email", "maintenance_mode")},
        ),
    )


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["site", "allow_registration", "max_users"]
    list_select_related = ["site"]


admin.site.unregister(Site)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
