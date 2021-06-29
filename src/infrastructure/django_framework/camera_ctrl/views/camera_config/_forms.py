from collections import OrderedDict
from typing import Iterable

from django import forms

from adapters.camera.configs.dtos import ConfigSectionDto, ConfigFieldDto, ConfigFieldType, ConfigsDto


class SingleConfigForm(forms.Form):
    def __init__(self, form_field: forms.Field, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = form_field
        self.name = name
        self.fields[name] = form_field

        self.tried_to_change = False
        self.managed_to_change = False

    @classmethod
    def from_config_dto(cls, config_dto: ConfigFieldDto, post_data: dict):
        form_field = _field_config_to_django_form_field(config_dto)

        if form_field is None:
            return None

        return cls(form_field, config_dto.name, post_data)

    def set_value(self, value):
        data_copy = self.data.copy()

        if isinstance(self.field, forms.BooleanField):
            if value:
                data_copy[self.name] = 'on'
            else:
                if self.name in data_copy:
                    data_copy.pop(self.name)

        else:
            data_copy[self.name] = value

        self.data = data_copy


class ConfigFormSection:
    def __init__(self, name: str, label: str, post_data):
        self.name = name
        self.label = label
        self.form_fields_dict = OrderedDict()

        self._post_data = post_data

    @property
    def form_fields(self) -> Iterable[SingleConfigForm]:
        return self.form_fields_dict.values()

    @property
    def has_errors(self) -> bool:
        for form_field in self.form_fields:
            if len(form_field.errors) != 0:
                return True

        return False

    @property
    def has_fields_that_did_not_manage_to_change(self) -> bool:
        for form_field in self.form_fields:
            if form_field.tried_to_change and not form_field.managed_to_change:
                return True

        return False

    @property
    def has_fields_that_manage_to_change(self) -> bool:
        for form_field in self.form_fields:
            if form_field.tried_to_change and form_field.managed_to_change:
                return True

        return False

    def add_fields(self, fields: Iterable[ConfigFieldDto]):
        for field in fields:
            form = SingleConfigForm.from_config_dto(config_dto=field, post_data=self._post_data)
            if form is None:
                continue
            self.form_fields_dict[field.name] = form


class CameraConfigFormManager:
    def __init__(self, post_data: dict):
        self._post_data = post_data
        self.sections_dict = OrderedDict()

    @property
    def sections(self) -> Iterable[ConfigFormSection]:
        return self.sections_dict.values()

    def load_from_configs_dto(self, configs: ConfigsDto):
        for section in configs.sections:
            self.add_fields_from_section(section_dto=section)

    def add_fields_from_section(self, section_dto: ConfigSectionDto):
        if section_dto.name in self.sections_dict:
            section = self.sections_dict[section_dto.name]
        else:
            section = ConfigFormSection(name=section_dto.name, label=section_dto.label, post_data=self._post_data)
            self.sections_dict[section_dto.name] = section

        section.add_fields(section_dto.fields)


def _field_config_to_django_form_field(config_field: ConfigFieldDto):
    if config_field is None:
        return None

    default_help_text = config_field.name

    if config_field.field_type == ConfigFieldType.TEXT:
        return forms.CharField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False,
            max_length=256,
            strip=False)

    if config_field.field_type == ConfigFieldType.CHOICE:
        return forms.ChoiceField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False,
            choices=((choice, choice) for choice in config_field.choices))

    if config_field.field_type == ConfigFieldType.TOGGLE:
        return forms.BooleanField(
            label=config_field.label,
            initial=(config_field.value != 0),
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False)

    if config_field.field_type == ConfigFieldType.RANGE:
        help_text = '{0}: [{1}, {2}]'.format(
            config_field.name,
            config_field.val_range.min_val,
            config_field.val_range.max_val)

        return forms.FloatField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=help_text,
            required=False,
            min_value=config_field.val_range.min_val,
            max_value=config_field.val_range.max_val)

    return None
