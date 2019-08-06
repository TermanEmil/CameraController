import os
from collections import OrderedDict
from typing import Iterable

from django import forms

from business.camera_control.camera_config import *
from camera_control.models import Profile, FavField, CronTimelapse


class CameraConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sections_dict = OrderedDict()

    @property
    def sections(self):
        return self.sections_dict.values()

    @property
    def visible_fields_dict(self) -> dict:
        return dict((field.name, field) for field in self.visible_fields())

    def load_from_camera_config(self, camera_config: CameraConfig):
        for section in camera_config.sections.values():
            assert isinstance(section, CameraConfigSection)
            self.add_fields(section.fields.values(), section.label, section.name)

    def add_fields(self, fields: Iterable[CameraConfigField], section_label, section_name):
        if section_name in self.sections_dict:
            section = self.sections_dict[section_name]
        else:
            section = CameraConfigSectionForm(section_label, section_name)
            self.sections_dict[section_name] = section

        section.add_fields(fields)
        self.fields.update(section.fields)
        section.set_visible_fields(self.visible_fields_dict)


class CameraConfigSectionForm:
    def __init__(self, section_label, section_name):
        self.label = section_label
        self.name = section_name
        self.visible_fields = []

        self.fields = {}

    def add_fields(self, fields: Iterable[CameraConfigField]):
        for field in fields:
            form_field = _field_config_to_django_form_field(field)

            if form_field is not None:
                self.fields[field.name] = form_field

    def set_visible_fields(self, visible_fields):
        for key, _ in self.fields.items():
            self.visible_fields.append(visible_fields[key])

        self.visible_fields.sort(key=lambda x: x.name)


class CameraSingleConfigForm(forms.Form):
    def __init__(self, config_field: CameraConfigField, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_field = _field_config_to_django_form_field(config_field)

        if form_field is not None:
            self.fields[config_field.name] = form_field


def _field_config_to_django_form_field(config_field: CameraConfigField):
    default_help_text = config_field.name

    if isinstance(config_field, CameraConfigTextField):
        return forms.CharField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False,
            max_length=256,
            strip=False,
        )

    if isinstance(config_field, CameraConfigChoiceField):
        return forms.ChoiceField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False,
            choices=((choice, choice) for choice in config_field.choices)
        )

    if isinstance(config_field, CameraConfigToggleField):
        return forms.BooleanField(
            label=config_field.label,
            initial=(config_field.value != 0),
            disabled=config_field.is_readonly,
            help_text=default_help_text,
            required=False,
        )

    if isinstance(config_field, CameraConfigRangeField):
        help_text = '{0}: [{1}, {2}]'.format(
            config_field.name,
            config_field.range_min,
            config_field.range_max)

        return forms.FloatField(
            label=config_field.label,
            initial=config_field.value,
            disabled=config_field.is_readonly,
            help_text=help_text,
            required=False,
            min_value=config_field.range_min,
            max_value=config_field.range_max,
        )

    return None


class FavConfigsProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name']


class FavConfigsFieldForm(forms.ModelForm):
    model_pk = None

    class Meta:
        model = FavField
        fields = ['name']


class CronTimelapseForm(forms.ModelForm):
    class Meta:
        model = CronTimelapse
        fields = [
            'name',
            'storage_dir_format',
            'filename_format',

            'start_date',
            'end_date',

            'second',
            'minute',
            'hour',
            'day_of_week',
            'week',
            'day',
            'month',
            'year',
        ]

        help_texts = {
            'storage_dir_format': 'Tilde (~) is short for home directory',

            'second': '0-59',
            'minute': '0-59',
            'hour': '0-23',
            'day_of_week': 'Number or name of weekday (0-6 or mon, tue, wed, thu, fri, sat, sun)',
            'week': '1-53',
            'day': '1-31',
            'month': '1-12',
            'year': '4 digit year'
        }

    def clean(self):
        super().clean()

        self.cleaned_data['storage_dir_format'] = os.path.expanduser(self.cleaned_data.get('storage_dir_format'))
