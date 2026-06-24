

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import service_unavailable_view
urlpatterns = [
    path("admin/", admin.site.urls),
 path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),

    path("blog/", include("blog.urls")),
    path("search/", include("search.urls")),
    path("service-unavailable/", service_unavailable_view, name="service-unavailable")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)