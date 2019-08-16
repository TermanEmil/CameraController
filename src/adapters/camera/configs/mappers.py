from typing import Optional

from enterprise.camera_ctrl.camera_config import *
from .dtos import *


def configs_to_dto(configs: CameraConfig) -> ConfigsDto:
    dto_sections = [config_section_to_dto(section) for section in configs.sections.values()]
    return ConfigsDto(sections=dto_sections)


def config_section_to_dto(section: CameraConfigSection) -> ConfigSectionDto:
    dto_fields = [config_field_to_dto(field) for field in section.fields.values() if field is not None]
    dto_fields = [field for field in dto_fields if field is not None]

    return ConfigSectionDto(name=section.name, label=section.label, fields=dto_fields)


def config_field_to_dto(field: CameraConfigField) -> Optional[ConfigFieldDto]:
    config_type = get_config_field_type(field)
    if config_type is None:
        return None

    dto = ConfigFieldDto(
        field_type=config_type,
        value=field.value,
        is_readonly=field.is_readonly,
        name=field.name,
        label=field.label)

    if isinstance(field, CameraConfigRangeField):
        dto.val_range = Range(min_val=field.range_min, max_val=field.range_max)
        if not (dto.val_range.min_val <= dto.value <= dto.val_range.max_val):
            return None

    if isinstance(field, CameraConfigChoiceField):
        dto.choices = field.choices
        if dto.value not in dto.choices:
            return None

    # Just remove an annoying field from Nikon cameras
    if 'date & time' in dto.label.lower():
        return None

    return dto


def get_config_field_type(field: CameraConfigField) -> Optional[ConfigFieldType]:
    if isinstance(field, CameraConfigChoiceField):
        return ConfigFieldType.CHOICE

    if isinstance(field, CameraConfigTextField):
        return ConfigFieldType.TEXT

    if isinstance(field, CameraConfigToggleField):
        return ConfigFieldType.TOGGLE

    if isinstance(field, CameraConfigRangeField):
        return ConfigFieldType.RANGE

    return None
