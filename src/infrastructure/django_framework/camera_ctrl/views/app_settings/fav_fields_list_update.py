from typing import Iterable

from django.views.generic import TemplateView

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from camera_ctrl.views.app_settings._forms import FavouriteConfigForm
from shared.di import obj_graph
from shared.mixins.error_utils_mixin import ErrorUtilsMixin
from django.contrib.auth.mixins import AccessMixin



class FavFieldsListUpdate(AccessMixin, TemplateView, ErrorUtilsMixin):
    template_name = 'app_settings/fav_fields_settings.html'
    favourite_configs_service: FavouriteConfigsService = obj_graph().provide(FavouriteConfigsService)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        context = self.get_context_data(**kwargs)

        fav_field_formset = list(self._create_formset(request=request))
        if request.method == 'POST':
            self.post(formset=fav_field_formset)

        context['formset'] = fav_field_formset
        return self.render_to_response(context=context)

    def post(self, formset: Iterable[FavouriteConfigForm]):
        for form in formset:
            if not (form.is_valid() and form.has_changed()):
                continue

            self.favourite_configs_service.update(pk=form.cleaned_data['pk'], config_name=form.cleaned_data['name'])

    def _create_formset(self, request):
        fav_fields = list(self.favourite_configs_service.get_all())

        for fav_field in fav_fields:
            initial = {'pk': fav_field.pk, 'name': fav_field.name}
            form = FavouriteConfigForm(request.POST or None, initial=initial, prefix='field_{}'.format(fav_field.pk))
            form.model_pk = fav_field.pk
            yield form