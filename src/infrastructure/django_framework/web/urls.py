from django.contrib import admin
from django.urls import path, include

from shared.utils.setup_startup import setup_startup
from .factories import startup_factory


setup_startup(lambda: startup_factory().run())


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('camera_ctrl.urls.urls')),
    path('camera_ctrl/', include('camera_ctrl.urls.urls')),
]
