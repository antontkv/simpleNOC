from django import forms

class SubnetsAddForm(forms.Form):
    subnets_to_add = forms.CharField(widget=forms.Textarea)
