from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Veritas Asset Recovery API is running!")

urlpatterns = [
    path('', home),  # 👈 Add this
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)