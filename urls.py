from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inclusion des URLs de l'application 'website'
    path('', include('website.urls')),
    
    # Inclusion des URLs de l'application 'users'
    # préfixe 'users/' pour  les URLs de users
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)