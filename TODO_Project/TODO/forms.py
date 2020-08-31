from django import forms

class CreateItemForm(forms.Form):
    title = forms.CharField(label='Title', max_length=80, required=True)
    completed = forms.BooleanField(initial=False, required=False)
