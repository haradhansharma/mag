# backend/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api.router import api  # Import the api instance

admin.site.site_header = "Meridian admin"
admin.site.site_title = "Meridian admin"
# admin.site.site_url = ''
admin.site.index_title = "Meridian administration"
# admin.empty_value_display = '**Empty**'

admin.autodiscover()
# admin.site.login = secure_admin_login(admin.site.login)  # type: ignore

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
