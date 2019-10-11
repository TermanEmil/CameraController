from django import forms


class FavouriteConfigForm(forms.Form):
    model_pk = None

    pk = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=124)