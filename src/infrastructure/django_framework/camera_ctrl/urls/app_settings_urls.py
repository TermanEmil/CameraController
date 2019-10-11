from django.urls import path

from camera_ctrl.api.app_settings.fav_field_add import FavFieldAdd
from camera_ctrl.api.app_settings.fav_field_remove import FavFieldRemove
from camera_ctrl.views.app_settings.fav_fields_list_update import FavFieldsListUpdate
from camera_ctrl.views.app_settings.general_settings_update_view import GeneralSettingsUpdateView
from camera_ctrl.views.app_settings.settings import Settings

urlpatterns = [
    path('', Settings.as_view(), name='settings'),

    path('fav_fields', FavFieldsListUpdate.as_view(), name='fav_fields'),
    path('fav_fields/add', FavFieldAdd.as_view(), name='fav_fields/add'),
    path('fav_fields/remove/<int:pk>', FavFieldRemove.as_view(), name='fav_fields/remove'),

    path('general_settings/<int:pk>', GeneralSettingsUpdateView.as_view(), name='general_settings')
]