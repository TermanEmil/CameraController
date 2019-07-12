import logging
from business.camera_config import CameraConfig, CameraConfigField, CameraConfigType, CameraConfigSection
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from .ids import *


class PreviewForm(forms.Form):
    preview_quality = forms.IntegerField(
        label='Preview quality',
        validators=[MinValueValidator(1), MaxValueValidator(100)])

    def get_preview_quality(self):
        return self.cleaned_data[c_preview_quality_id]


class CameraConfigForm(forms.Form):
    def __init__(self, camera_config, *args, **kwargs):
        super(CameraConfigForm, self).__init__(*args, **kwargs)
        assert isinstance(camera_config, CameraConfig)

        self.sections = []
        for section in camera_config.sections:
            section_form = CameraConfigSectionForm(section)
            self.fields.update(section_form.fields)
            self.sections.append(section_form)

        # Apparently, I can only render fields from visible_fields.
        visible_fields_dict = dict((field.name, field) for field in self.visible_fields())
        for section in self.sections:
            assert isinstance(section, CameraConfigSectionForm)
            section.set_visible_fields(visible_fields_dict)


class CameraConfigSectionForm:
    def __init__(self, section):
        assert isinstance(section, CameraConfigSection)

        self.fields = dict(_config_section_to_django_form(section))
        self.label = section.label
        self.name = section.name
        self.is_readonly = section.is_readonly
        self.visible_fields = []

    def set_visible_fields(self, visible_fields):
        for key, _ in self.fields.items():
            self.visible_fields.append(visible_fields[key])

        self.visible_fields.sort(key=lambda x: x.name)


def _config_section_to_django_form(section):
    assert isinstance(section, CameraConfigSection)

    for key, field in section.fields_dict.items():
        assert isinstance(field, CameraConfigField)

        form_field = _field_config_to_django_form_field(field)
        if form_field is None:
            logging.warning('Failed to create form field for: {0}'.format(key))
            continue

        yield (key, form_field)


def _field_config_to_django_form_field(field_config):
    assert isinstance(field_config, CameraConfigField)

    config = field_config
    default_help_text = '{0}/{1}'.format(config.parent_widget.name, config.name)

    if config.config_type == CameraConfigType.TEXT:
        return forms.CharField(
            label=config.label,
            initial=config.value,
            disabled=config.is_readonly,
            help_text=default_help_text,
            required=False,
            max_length=256,
        )

    if config.config_type == CameraConfigType.MENU or config.config_type == CameraConfigType.RADIO:
        return forms.ChoiceField(
            label=config.label,
            initial=config.value,
            disabled=config.is_readonly,
            help_text=default_help_text,
            required=False,
            choices=((choice, choice) for choice in config.choices)
        )

    if config.config_type == CameraConfigType.TOGGLE:
        return forms.BooleanField(
            label=config.label,
            initial=(config.value != 0),
            disabled=config.is_readonly,
            help_text=default_help_text,
            required=False,
        )

    if config.config_type == CameraConfigType.DATE:
        return forms.IntegerField(
            label=config.label,
            initial=config.value,
            disabled=config.is_readonly,
            help_text=default_help_text,
            required=False,
        )

    if config.config_type == CameraConfigType.RANGE:
        help_text = '{0}/{1}: [{2}, {3}]'.format(
            config.parent_widget.name,
            config.name,
            config.range_min,
            config.range_max)

        return forms.FloatField(
            label=config.label,
            initial=config.value,
            disabled=config.is_readonly,
            help_text=help_text,
            required=False,
            min_value=config.range_min,
            max_value=config.range_max,
        )

    return None
