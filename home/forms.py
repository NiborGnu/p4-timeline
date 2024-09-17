from django import forms
from .models import TimePost, Comment


class TimePostForm(forms.ModelForm):
    """
    Form for creating or updating a TimePost.
    """
    # Define a field for the body of the TimePost
    body = forms.CharField(
        # Specify that this field is required
        required=True,
        # Configure the widget for this field as a textarea
        widget=forms.Textarea(
            attrs={
                # Placeholder text to prompt the user
                'placeholder': "What's happening today?",
                # CSS class for styling
                'class': 'form-control',
                # Set the default height of the textarea
                'rows': 4,
                # Accessible label for screen readers
                'aria-label': 'TimePost body',
            }
        ),
        # Leave the label empty to use the placeholder as the visible prompt
        label="",
    )

    class Meta:
        """
        Metadata for the TimePostForm.
        """
        # Specify the model associated with this form
        model = TimePost
        # Exclude fields that should not be included in the form
        exclude = ('user', 'likes', 'dislikes')


class CommentForm(forms.ModelForm):
    """
    Form for creating or updating a Comment.
    """
    # Define a field for the body of the comment
    body = forms.CharField(
        # Specify that this field is required
        required=True,
        # Configure the widget for this field as a textarea
        widget=forms.Textarea(
            attrs={
                # Placeholder text to prompt the user
                'placeholder': 'Add a comment...',
                # CSS class for styling
                'class': 'form-control',
                # Set the default height of the textarea
                'rows': 3,
                # Accessible label for screen readers
                'aria-label': 'Comment body',
            }
        ),
        # Leave the label empty to use the placeholder as the visible prompt
        label="",
    )

    class Meta:
        """
        Metadata for the CommentForm.
        """
        # Specify the model associated with this form
        model = Comment
        # Include only the 'body' field in the form
        fields = ['body']
