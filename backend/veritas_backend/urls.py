from abc import ABC, abstractmethod

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


class Settings(ABC):
    @property
    @abstractmethod
    def debug(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def media_url(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def media_root(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def allowed_hosts(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def csrf_trusted_origins(self):
        raise NotImplementedError

    def as_dict(self):
        return {
            'DEBUG': self.debug,
            'MEDIA_URL': self.media_url,
            'MEDIA_ROOT': self.media_root,
            'ALLOWED_HOSTS': self.allowed_hosts,
        }


class DjangoSettings(Settings):
    @property
    def debug(self):
        return settings.DEBUG

    @property
    def media_url(self):
        return settings.MEDIA_URL

    @property
    def media_root(self):
        return settings.MEDIA_ROOT

    @property
    def allowed_hosts(self):
        return settings.ALLOWED_HOSTS


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_settings = DjangoSettings()