# excavator_parts_shop/urls.py

from django.contrib import admin
from django.urls import path, include  # Make sure to import path and include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # Assuming 'shop' is your app
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
