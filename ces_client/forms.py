from django import forms

class ResponseForm(forms.Form):
    response = forms.CharField(label='response', max_length=100)