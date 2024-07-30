from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=50)


class RegionForm(forms.Form):
    regionfile = forms.FileField()