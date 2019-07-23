from business.camera_control.camera_config import CameraConfigField
from camera_control.models import Profile, FavField
from business.camera_control.camera import Camera


class FavConfigsManager:
    _c_fav_config_profile_id = 'fav_config_profile'

    def get_profile(self, request) -> Profile:
        profile_name = request.session.get(self._c_fav_config_profile_id, 'default')
        profile = Profile.objects.filter(name=profile_name).first()
        if profile is None:
            profile = Profile.build_default_profile()

        self.set_profile(request, profile)
        return profile

    def set_profile(self, request, profile: Profile):
        request.session[self._c_fav_config_profile_id] = profile.name

    def extract_configs(self, profile: Profile, camera: Camera) -> CameraConfigField:
        for field in profile.fields.all():
            assert isinstance(field, FavField)

            config = camera.get_single_config(field.name_pattern)
            if config is None:
                continue

            yield config
