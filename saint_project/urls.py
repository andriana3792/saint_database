from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path("saints-dashboard/", admin.site.urls),
    path("", include("saints.urls")),  # root URL handled by saints.urls
]

# Serve default media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Serve custom saint_images folder
    CUSTOM_IMAGE_URL = "/saint_images/"
    CUSTOM_IMAGE_ROOT = os.path.join(settings.BASE_DIR, "saint_images")
    urlpatterns += static(CUSTOM_IMAGE_URL, document_root=CUSTOM_IMAGE_ROOT)
