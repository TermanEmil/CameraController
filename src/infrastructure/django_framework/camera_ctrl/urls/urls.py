from django.urls import path, include

from camera_ctrl.startup.app_startup import AppStartup
from camera_ctrl.urls import camera_ctrl_urls
from shared.di import obj_graph
from shared.utils.setup_startup import setup_startup

setup_startup(lambda: obj_graph().provide(AppStartup).run())

urlpatterns = [
    path('camera_config/', include('camera_ctrl.urls.camera_config_urls')),
    path('scheduling/', include('camera_ctrl.urls.scheduling_urls')),
    path('logging/', include('camera_ctrl.urls.app_logging_urls')),
    path('settings/', include('camera_ctrl.urls.app_settings_urls')),
]

urlpatterns += camera_ctrl_urls.urlpatterns