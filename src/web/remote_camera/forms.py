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


class CameraConfigSectionForm(forms.Form):
    def __init__(self, section_config):
        super().__init__()
        assert isinstance(section_config, CameraConfig)

        self.prefix = section_config.name

        if section_config.child_configs is None:
            return

        for config in section_config.child_configs:
            assert isinstance(config, CameraConfig)

            if config.config_type == CameraConfigType.TEXT:
                self.fields[config.name] = forms.CharField(
                    label=config.label,
                    initial=config.value,
                    disabled=config.is_readonly,
                    max_length=256,
                    help_text=config.name
                )

