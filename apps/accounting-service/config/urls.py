import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.swagger import urlpatterns as swagger_urlpattern

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        *swagger_urlpattern,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]

if settings.TOOLBAR:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
