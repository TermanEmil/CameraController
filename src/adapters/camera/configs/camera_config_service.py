from typing import Iterable

from business.camera.config.get_all_config_names_bl_rule import GetAllConfigNamesBlRule
from business.camera.config.get_all_configs_bl_rule import GetAllConfigsBlRule
from business.camera.config.get_config_bl_rule import GetConfigBlRule
from business.camera.config.set_config_bl_rule import SetConfigBlRule
from .dtos import ConfigFieldDto
from .favourite_configs_repository import FavouriteConfigsRepository
from .mappers import configs_to_dto, config_field_to_dto, ConfigsDto


class CameraConfigService:
    def __init__(
            self,
            favourite_config_repository: FavouriteConfigsRepository,
            get_all_configs_bl_rule: GetAllConfigsBlRule,
            get_all_config_names_bl_rule: GetAllConfigNamesBlRule,
            get_config_bl_rule: GetConfigBlRule,
            set_config_bl_rule: SetConfigBlRule):

        self._favourite_config_repository = favourite_config_repository
        self._get_all_bl_rule = get_all_configs_bl_rule
        self._get_all_config_names_bl_rule = get_all_config_names_bl_rule
        self._get_config_bl_rule = get_config_bl_rule
        self._set_config_bl_rule = set_config_bl_rule

    def get_all_configs(self, camera_id: str) -> ConfigsDto:
        configs = self._get_all_bl_rule.set_params(camera_id=camera_id).execute()
        dto = configs_to_dto(configs=configs)
        dto.sections = [section for section in dto.sections if section.name != 'other']
        return dto

    def get_all_config_names(self, camera_id: str) -> Iterable[str]:
        return self._get_all_config_names_bl_rule.set_params(camera_id=camera_id).execute()

    def get_config(self, camera_id: str, config_name: str) -> ConfigFieldDto:
        config_field = self._get_config_bl_rule.set_params(camera_id=camera_id, config_name=config_name).execute()
        return config_field_to_dto(field=config_field)

    def set_config(self, camera_id: str, config_name: str, config_value: str):
        self._set_config_bl_rule \
            .set_params(camera_id=camera_id, config_name=config_name, config_value=config_value) \
            .execute()

    def get_favourite_configs(self, camera_id: str) -> Iterable[ConfigFieldDto]:
        favourite_fields = self._favourite_config_repository.get_all()

        for fav_field in favourite_fields:
            try:
                config = self.get_config(camera_id=camera_id, config_name=fav_field.name)
                yield config

            except:
                continue

