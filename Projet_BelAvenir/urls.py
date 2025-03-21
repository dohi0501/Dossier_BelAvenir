
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'App_BelAvenir.views.erreur_404'

urlpatterns = [
    path('admin/benito2024/', admin.site.urls),
    path('', include('App_BelAvenir.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
