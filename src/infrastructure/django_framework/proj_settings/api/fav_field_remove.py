from django.http import HttpResponseServerError, HttpResponse
from django.views.generic import DeleteView

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService


class FavFieldRemove(DeleteView):
    favourite_configs_service: FavouriteConfigsService = None

    def delete(self, request, *args, **kwargs):
        fav_field_pk = kwargs['pk']

        try:
            self.favourite_configs_service.remove(pk=int(fav_field_pk))
            return HttpResponse(status=200)

        except Exception as e:
            return HttpResponseServerError(content=str(e))
