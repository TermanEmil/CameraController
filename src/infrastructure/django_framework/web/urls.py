from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('camera_ctrl.urls')),
    path('camera_ctrl/', include('camera_ctrl.urls')),
    path('camera_config/', include('camera_config.urls')),
    path('settings/', include('proj_settings.urls')),
    path('scheduling/', include('scheduling.urls')),
]
