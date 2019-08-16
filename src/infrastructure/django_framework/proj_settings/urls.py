from django.urls import path

from .factories import *
from .views.settings import Settings

urlpatterns = [
    path('', Settings.as_view(), name='settings'),

    path('fav_fields', fav_fields_settings_view_factory(), name='fav_fields'),
    path('fav_fields/add', fav_field_add_view_factory(), name='fav_fields/add'),
    path('fav_fields/remove/<int:pk>', fav_field_remove_view_factory(), name='fav_fields/remove'),
]