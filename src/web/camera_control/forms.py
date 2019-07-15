from business.camera_control.camera_config import *
from django import forms


class CameraConfigForm(forms.Form):
    def __init__(self, config: CameraConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sections = []
        for _, section in config.sections.items():
            section_form = CameraConfigSectionForm(section)
            self.fields.update(section_form.fields)
            self.sections.append(section_form)

        # Apparently, I can only render fields from visible_fields.
        self.visible_fields_dict = dict((field.name, field) for field in self.visible_fields())
        for section in self.sections:
            assert isinstance(section, CameraConfigSectionForm)
            section.set_visible_fields(self.visible_fields_dict)


class CameraConfigSectionForm:
    def __init__(self, section: CameraConfigSection):
        self.label = section.label
        self.name = section.name
        self.visible_fields = []

        self.fields = {}
        for _, field in section.fields.items():
            assert isinstance(field, CameraConfigField)
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
