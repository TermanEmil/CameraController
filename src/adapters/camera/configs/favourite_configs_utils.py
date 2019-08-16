from typing import Iterable

from .favourite_configs_repository import FavouriteConfig
from .dtos import ConfigsDto, ConfigSectionDto


def create_favourite_section_dto(configs: ConfigsDto, favourite_fields: Iterable[FavouriteConfig]) -> ConfigSectionDto:
    favourite_configs = _extract_favourite_field_dtos(configs=configs, favourite_fields=favourite_fields)
    return ConfigSectionDto(name='favourite', label='Favourite configs', fields=favourite_configs)


def _extract_favourite_field_dtos(configs: ConfigsDto, favourite_fields: Iterable[FavouriteConfig]):
    for fav_field in favourite_fields:
        for section in configs.sections:
            for field in section.fields:
                if field.name == fav_field.name:
                    yield field