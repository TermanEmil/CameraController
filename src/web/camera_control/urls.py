from django.urls import path

from views.index import index
from views.camera_search import camera_search
from views.config_list import config_list
from views.single_config import single_config
from views.all_configs import all_configs
from views.live_preview import live_preview
from views.live_preview_source import live_preview_source
from views.multi_live_preview import multi_live_preview
from views.capture_img_and_download import capture_img_and_download
from views.camera_remove import camera_remove


urlpatterns = [
    path('', index, name='index'),
    path('camera_search', camera_search, name='camera_search'),
    path('config_list/<str:camera_id>', config_list, name='config_list'),
    path('single_config/<str:camera_id>/<str:config_name>', single_config, name='single_config'),
    path('all_configs/<str:camera_id>', all_configs, name='all_configs'),
    path('live_preview/<str:camera_id>', live_preview, name='live_preview'),
    path('live_preview_source/<str:camera_id>', live_preview_source, name='live_preview_source'),
    path('multi_live_preview', multi_live_preview, name='multi_live_preview'),
    path('capture_img_and_download/<str:camera_id>', capture_img_and_download, name='capture_img_and_download'),
    path('camera_remove/<str:camera_id>', camera_remove, name='camera_remove'),
]
