from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Nii Kpakpo Campaign — Admin"
admin.site.site_title = "Campaign Admin"
admin.site.index_title = "Manage Campaign Content"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
