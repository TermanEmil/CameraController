from typing import Iterable

from django.views.generic import TemplateView

from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from shared.mixins.error_utils_mixin import ErrorUtilsMixin
from ..forms import FavouriteConfigForm


class FavFieldsListUpdate(TemplateView, ErrorUtilsMixin):
    template_name = 'proj_settings/fav_fields_settings.html'
    favourite_configs_service: FavouriteConfigsService = None

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            fav_field_formset = list(self._create_formset(request=request))
            if request.method == 'POST':
                self.post(formset=fav_field_formset)

        except Exception as e:
            return self.render_to_error(request=request, error=str(e))

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