from django.urls import path

from proj_settings.views.general_settings import GeneralSettingsUpdateView
from .factories import *
from .views.settings import Settings

urlpatterns = [
    path('', Settings.as_view(), name='settings'),

    path('fav_fields', fav_fields_settings_view_factory(), name='fav_fields'),
    path('fav_fields/add', fav_field_add_view_factory(), name='fav_fields/add'),
    path('fav_fields/remove/<int:pk>', fav_field_remove_view_factory(), name='fav_fields/remove'),

    path('general_settings/<int:pk>', GeneralSettingsUpdateView.as_view(), name='general_settings')
]