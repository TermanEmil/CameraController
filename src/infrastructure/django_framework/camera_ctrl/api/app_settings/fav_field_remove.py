from django.http import HttpResponse
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from shared.di import obj_graph


class FavFieldRemove(LoginRequiredMixin, DeleteView):
    favourite_configs_service = obj_graph().provide(FavouriteConfigsService)

    def delete(self, request, *args, **kwargs):
        fav_field_pk = kwargs['pk']

        self.favourite_configs_service.remove(pk=int(fav_field_pk))
        return HttpResponse(status=200)
