from django import forms

class SuperviseeForm(forms.Form):
    id = forms.IntegerField()