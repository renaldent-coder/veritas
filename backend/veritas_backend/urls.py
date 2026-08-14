from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# 👇 Add this home view
def home(request):
    return HttpResponse("Veritas Asset Recovery API is running!")

urlpatterns = [
    path('', home),  # 👈 Add this line
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)