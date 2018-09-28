from django import forms

class UserForm(forms.Form):
    email = forms.CharField(required = True)
    order = forms.CharField(required = True)