from django import forms
from import_data import models


class ImportFileForm(forms.Form):
    file = forms.FileField()
