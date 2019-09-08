from django.contrib import admin
from django.urls import path, include

from shared.utils.setup_startup import setup_startup
from .factories import *


setup_startup(lambda: startup_factory().run())


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('camera_ctrl.urls')),
    path('camera_ctrl/', include('camera_ctrl.urls')),
    path('camera_config/', include('camera_config.urls')),
    path('settings/', include('proj_settings.urls')),
    path('scheduling/', include('scheduling.urls')),
    path('logging/', include('proj_logging.urls')),
    path('file_transfer/', include('file_transfer.urls')),
]
