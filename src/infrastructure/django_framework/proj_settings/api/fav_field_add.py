from django.http import HttpResponseServerError, HttpResponse
from django.views.generic import View

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService


class FavFieldAdd(View):
    favourite_configs_service: FavouriteConfigsService = None

    def get(self, request, *args, **kwargs):
        try:
            self.favourite_configs_service.add_dummy()
            return HttpResponse(status=201)

        except Exception as e:
            return HttpResponseServerError(content=str(e))
