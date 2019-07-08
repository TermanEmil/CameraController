from django.urls import path

from .views import index, live_preview, live_preview_source, search_for_cameras, camera_config


urlpatterns = [
    path('', index.index, name='index'),
    path('live_preview_source/<str:camera_port>', live_preview_source.live_preview_source, name='live_preview_source'),
    path('live_preview/<str:camera_port>', live_preview.live_preview, name='live_preview'),
    path('multi_live_preview/', live_preview.multi_live_preview, name='multi_live_preview'),
    path('search_for_cameras/', search_for_cameras.search_for_cameras, name='search_for_cameras'),
    path('camera_config/<str:camera_port>', camera_config.camera_config, name='camera_config'),
]
