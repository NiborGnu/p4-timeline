from django import forms
from .models import TimePost, Comment


class TimePostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': "What's happening today?",
                'class': 'form-control',
                'rows': 4,  # Set default height of textarea
                'aria-label': 'TimePost body',
            }
        ),
        label="",
    )

    class Meta:
        model = TimePost
        exclude = ('user', 'likes', 'dislikes')


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control',
                'rows': 3,  # Set default height of textarea
                'aria-label': 'Comment body',
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ['body']
