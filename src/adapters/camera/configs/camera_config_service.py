from typing import Iterable

from business.camera.exceptions import CameraNotFoundException, ConfigNotFoundException, InvalidConfigException
from enterprise.camera_ctrl.camera_manager import CameraManager
from enterprise.camera_ctrl.exceptions import InvalidConfigException as EnterpriseInvalidConfigException
from .dtos import ConfigFieldDto, ConfigSectionDto
from .favourite_configs_repository import FavouriteConfigsRepository
from .mappers import configs_to_dto, config_field_to_dto, ConfigsDto


class CameraConfigService:
    def __init__(
            self,
            camera_manager: CameraManager,
            favourite_config_repository: FavouriteConfigsRepository):

        self._camera_manager = camera_manager
        self._favourite_config_repository = favourite_config_repository

    def get_all_configs(self, camera_id) -> ConfigsDto:
        camera = self._get_camera(camera_id)
        configs = camera.get_config()
        dto = configs_to_dto(configs=configs)
        dto.sections = list(self._filter_unwanted_sections(dto.sections))
        return dto

    def get_all_config_names(self, camera_id) -> Iterable[str]:
        camera = self._get_camera(camera_id)
        return camera.list_configs()

    def get_config(self, camera_id, config_name: str) -> ConfigFieldDto:
        _, config = self._get_cam_and_config(camera_id, config_name)
        return config_field_to_dto(field=config)

    def set_config(self, camera_id, config_name: str, config_value: str):
        camera, config = self._get_cam_and_config(camera_id, config_name)

        try:
            config.set_value(value=config_value)
        except EnterpriseInvalidConfigException as e:
            raise InvalidConfigException(config_name=config_name, details=str(e))

        camera.set_config((config,))

    def get_favourite_configs(self, camera_id: str) -> Iterable[ConfigFieldDto]:
        camera = self._get_camera(camera_id)
        favourite_fields = self._favourite_config_repository.get_all()

        for fav_config in favourite_fields:
            config = camera.get_single_config(config_name=fav_config.name)
            if config is None:
                continue

            yield config_field_to_dto(field=config)

    @staticmethod
    def _filter_unwanted_sections(sections: Iterable[ConfigSectionDto]):
        for section in sections:
            if section.name != 'other':
                yield section

    def _get_camera(self, camera_id):
        camera = self._camera_manager.get_camera(camera_id=camera_id)
        if camera is None:
            raise CameraNotFoundException()

        return camera

    def _get_cam_and_config(self, camera_id, config_name: str):
        camera = self._get_camera(camera_id)
        config = camera.get_single_config(config_name=config_name)

        if config is None:
            raise ConfigNotFoundException(config_name)

        return camera, config
