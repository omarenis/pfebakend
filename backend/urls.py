from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from backend import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('gestionusers.views')),
    path(r'', include('form.views'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
