from django.urls import path
from .views import index, live_preview, live_preview_source


urlpatterns = [
    path('', index.index, name='index'),
    path('live_preview_source/<str:camera_port>', live_preview_source.live_preview_source, name='live_preview_source'),
    path('live_preview/<str:camera_port>', live_preview.live_preview, name='live_preview'),
]
