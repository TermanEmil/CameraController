from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from .api.fav_field_remove import FavFieldRemove
from .api.fav_field_add import FavFieldAdd
from shared.di import obj_graph
from .views.fav_fields_list_update import FavFieldsListUpdate


def fav_fields_settings_view_factory():
    favourite_configs_service = obj_graph().provide(FavouriteConfigsService)
    return FavFieldsListUpdate.as_view(favourite_configs_service=favourite_configs_service)


def fav_field_add_view_factory():
    favourite_configs_service = obj_graph().provide(FavouriteConfigsService)
    return FavFieldAdd.as_view(favourite_configs_service=favourite_configs_service)


def fav_field_remove_view_factory():
    favourite_configs_service = obj_graph().provide(FavouriteConfigsService)
    return FavFieldRemove.as_view(favourite_configs_service=favourite_configs_service)