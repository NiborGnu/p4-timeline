from django import forms
from .models import TimePost

class TimePostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Whats happening today?',
                'class': 'form-control',
            }
        ),
            label="",
    )

    # TODO: Add a image field to the form

    class Meta:
        model = TimePost
        exclude = ('user',)