from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .ids import *


class PreviewForm(forms.Form):
    preview_quality = forms.IntegerField(
        label='Preview quality',
        validators=[MinValueValidator(1), MaxValueValidator(100)])

    def get_preview_quality(self):
        return self.cleaned_data[c_preview_quality_id]
