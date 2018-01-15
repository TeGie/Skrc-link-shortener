from django import forms


class SubmitUrlForm(forms.Form):
    url = forms.URLField(
        label='',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'URL',
                'class': 'form-control'
            }
        )
    )
