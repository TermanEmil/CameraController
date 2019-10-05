from django.http import HttpResponse
from django.views.generic import View

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from shared.di import obj_graph


class FavFieldAdd(View):
    default_dummy_value = 'shutterspeed'
    favourite_configs_service = obj_graph().provide(FavouriteConfigsService)

    def get(self, request, *args, **kwargs):
        self.favourite_configs_service.add(config_name=self.default_dummy_value)
        return HttpResponse(status=201)
