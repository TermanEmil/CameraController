from django.http import HttpResponseRedirect
from django.shortcuts import render

from camera_control.models import Profile, FavField
from forms import FavConfigsProfileForm, FavConfigsFieldForm
from ..object_not_found import object_not_found
from factories import FavConfigsManagerFactory


def favourite_configs_profiles(request):
    profiles = list(Profile.objects.all())
    if len(profiles) == 0:
        profiles.append(Profile.build_default_profile())

    context = {
        'profiles': [ProfileViewModel(profile) for profile in profiles]
    }
    return render(request, 'camera_control/app_settings/favourite_configs_profiles.html', context)


def favourite_configs_profile(request, profile_id):
    profile = Profile.objects.filter(pk=profile_id).first()
    if profile is None:
        return object_not_found(request, 'Could not find the requested profile')

    profile_form = FavConfigsProfileForm(request.POST or None, instance=profile, prefix='profile')

    field_forms = []
    for field in profile.fields.all():
        field_form = FavConfigsFieldForm(request.POST or None, instance=field, prefix='field_{0}'.format(field.pk))
        field_form.model_pk = field.pk
        field_forms.append(field_form)

    fav_configs_manager = FavConfigsManagerFactory.get()
    current_profile = fav_configs_manager.get_profile(request)

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()

        for field_form in field_forms:
            if field_form.is_valid():
                field_form.save()

    if current_profile.pk == profile.pk:
        fav_configs_manager.set_profile(request, profile)

    context = {
        'profile_id': profile_id,
        'profile_form': profile_form,
        'field_forms': field_forms
    }
    return render(request, 'camera_control/app_settings/favourite_configs_profile.html', context)


def favourite_configs_profile_add_new(request, profile_id):
    profile = Profile.objects.filter(pk=profile_id).first()
    if profile is None:
        return object_not_found(request, 'Could not find the requested profile')

    new_field = FavField()
    new_field.profile = profile
    new_field.name_pattern = 'This can be a regex pattern'
    new_field.label = 'New field'
    new_field.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def favourite_configs_profile_remove(request, field_id):
    field = FavField.objects.filter(pk=field_id).first()
    if field is None:
        return object_not_found(request, 'Could not find the requested field')

    field.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProfileViewModel:
    def __init__(self, profile: Profile):
        self.name = profile.name
        self.pk = profile.pk