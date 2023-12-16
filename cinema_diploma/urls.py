from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cinema_diploma import settings

urlpatterns = [
    path('', include('cinema.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('users.API.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
