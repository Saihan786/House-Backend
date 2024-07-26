from django import forms

class RegionForm(forms.Form):
    title = forms.CharField(max_length=50)
    regionfile = forms.FileField()