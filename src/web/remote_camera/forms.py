from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from .ids import *
from business.CameraWrapper import CameraConfig, CameraConfigType


class PreviewForm(forms.Form):
    preview_quality = forms.IntegerField(
        label='Preview quality',
        validators=[MinValueValidator(1), MaxValueValidator(100)])

    def get_preview_quality(self):
        return self.cleaned_data[c_preview_quality_id]


class CameraConfigForm(forms.Form):
    def __init__(self, fields):
        super().__init__()
        for key, field in fields.items():
            self.fields[key] = field

    @staticmethod
    def extract_fields_for_camera_config_section(section_config):
        assert isinstance(section_config, CameraConfig)

        if section_config.child_configs is None:
            return []

        fields = {}
        for config in section_config.child_configs:
            assert isinstance(config, CameraConfig)
            field_name = '{0}/{1}'.format(section_config.name, config.name)

            if config.config_type == CameraConfigType.TEXT:
                fields[field_name] = forms.CharField(
                    label=config.label,
                    initial=config.value,
                    disabled=config.is_readonly,
                    help_text=field_name,
                    max_length=256,
                )
            elif config.config_type == CameraConfigType.MENU or config.config_type == CameraConfigType.RADIO:
                fields[field_name] = forms.ChoiceField(
                    label=config.label,
                    initial=config.value,
                    disabled=config.is_readonly,
                    help_text=field_name,
                    choices=((choice, choice) for choice in config.choices)
                )

        return fields
