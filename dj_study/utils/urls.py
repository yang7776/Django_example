from django.contrib import admin
from django.urls import path,include
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include("app1.urls")),
    path('app2/', include("app2.urls")),
    path('dwebsocket_/', include("dwebsocket_.urls")),
    path('channels_/', include("channels_.urls")),
    path('view_cbv/', include("view_CBV.urls")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
