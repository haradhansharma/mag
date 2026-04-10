from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

from common.models import (
    SiteConfig,
    SiteSettings,
    Article,
    Author,
    Category,
    Edition,
    PrintOrder,
)


# --- Site ---


class SiteConfigAdmin(SiteAdmin):
    list_display = ["domain", "name", "site_title", "support_email", "maintenance_mode"]


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["site", "allow_registration", "max_users"]
    list_select_related = ["site"]


admin.site.unregister(Site)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)


# --- Category ---


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color", "access", "featured", "article_count"]
    list_filter = ["access", "color", "featured"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


# --- Author ---


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "role", "article_count", "user"]
    list_filter = ["role"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["user"]


# --- Article ---


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "author",
        "category",
        "status",
        "content_type",
        "access",
        "featured",
        "trending",
        "pinned",
        "reading_time",
        "word_count",
        "published_at",
    ]
    list_filter = [
        "status",
        "content_type",
        "access",
        "featured",
        "trending",
        "pinned",
        "category",
    ]
    search_fields = ["title", "slug", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ["author", "category"]
    date_hierarchy = "published_at"


# --- Edition ---


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "title",
        "slug",
        "status",
        "print_ready",
        "article_count",
        "week_start",
        "week_end",
    ]
    list_filter = ["status", "print_ready"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


# --- Print Order ---


@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "user",
        "edition",
        "quantity",
        "total",
        "shipping_region",
        "status",
        "created_at",
    ]
    list_filter = ["status", "shipping_region"]
    search_fields = ["order_id", "first_name", "last_name"]
    list_select_related = ["user", "edition"]
    date_hierarchy = "created_at"
