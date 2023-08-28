from chat.routing import websocket_urlpatterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('ws/', include(websocket_urlpatterns))
]
