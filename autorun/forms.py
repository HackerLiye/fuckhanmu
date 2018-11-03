from django import forms


class RunForm(forms.Form):
    IMEI = forms.TimeField()