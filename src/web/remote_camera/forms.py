from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class PreviewSettingsForm(forms.Form):
    quality = forms.IntegerField(label='preview_quality', validators=[MinValueValidator(1), MaxValueValidator(100)])
