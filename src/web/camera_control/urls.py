from django.urls import path

from views.index import index
from views.camera_search import camera_search
from views.camera_config.config_list import config_list
from views.camera_config.single_config import single_config
from views.camera_config.all_configs import all_configs
from views.preview.live_preview import live_preview
from views.preview.live_preview_source import live_preview_source
from views.preview.multi_live_preview import multi_live_preview
from views.capture_img_and_download import capture_img_and_download
from views.camera_remove import camera_remove
from views.object_not_found import camera_not_found
from views.camera_reconnect import camera_reconnect
from views.app_settings.app_settings import app_settings
from views.app_settings.favourite_configs_profiles import *
from views.timelapse.timelapse_create import timelapse_create


urlpatterns = [
    path('', index, name='index'),
    path('camera_not_found', camera_not_found, name='camera_not_found'),

    path('camera_search', camera_search, name='camera_search'),
    path('camera_remove/<str:camera_id>', camera_remove, name='camera_remove'),
    path('camera_reconnect/<str:camera_id>', camera_reconnect, name='camera_reconnect'),

    path('config_list/<str:camera_id>', config_list, name='config_list'),
    path('single_config/<str:camera_id>/<str:config_name>', single_config, name='single_config'),
    path('all_configs/<str:camera_id>', all_configs, name='all_configs'),

    path('live_preview/<str:camera_id>', live_preview, name='live_preview'),
    path('live_preview_source/<str:camera_id>', live_preview_source, name='live_preview_source'),
    path('multi_live_preview', multi_live_preview, name='multi_live_preview'),

    path('capture_img_and_download/<str:camera_id>', capture_img_and_download, name='capture_img_and_download'),

    path('settings', app_settings, name='settings'),
    path('settings/favourite_configs_profiles', favourite_configs_profiles, name='settings/favourite_configs_profiles'),
    path(
        'settings/favourite_configs_profile/<int:profile_id>',
        favourite_configs_profile,
        name='settings/favourite_configs_profile'),
    path(
        'settings/favourite_configs_profile_add_new/<int:profile_id>',
        favourite_configs_profile_add_new,
        name='settings/favourite_configs_profile_add_new'),
    path(
        'settings/favourite_configs_profile_remove/<int:field_id>',
        favourite_configs_profile_remove,
        name='settings/favourite_configs_profile_remove'),

    path('timelapse/timelapse_create', timelapse_create, name='timelapse/timelapse_create'),
]
