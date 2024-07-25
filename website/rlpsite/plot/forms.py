from django import forms

class RegionForm(forms.Form):
    region = forms.FileField()