from django import forms


class NewGameForm(forms.Form):
    mode = forms.HiddenInput()