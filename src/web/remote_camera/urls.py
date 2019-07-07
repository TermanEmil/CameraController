from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('live_preview_source/<str:camera_port>', views.live_preview_source, name='live_preview_source'),
    path('live_preview/<str:camera_port>', views.live_preview, name='live_preview'),
]
