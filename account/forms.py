from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class SignUpForm(UserCreationForm):
    # Define additional fields for the form
    email = forms.EmailField(
        # No label displayed
        label='',
        widget=forms.TextInput(
            attrs={
                # CSS class for styling
                'class': 'form-control',
                # Placeholder text
                'placeholder': 'Email Address'
            }
        )
    )
    first_name = forms.CharField(
        # No label displayed
        label='',
        max_length=20,  # Max length for the field
        widget=forms.TextInput(
            attrs={
                # CSS class for styling
                'class': 'form-control',
                # Placeholder text
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        # No label displayed
        label='',
        max_length=20,  # Max length for the field
        widget=forms.TextInput(
            attrs={
                # CSS class for styling
                'class': 'form-control',
                # Placeholder text
                'placeholder': 'Last Name'
            }
        )
    )

    # Enforce min and max length for the username
    username = forms.CharField(
        label='',
        max_length=15,
        min_length=3,
        validators=[
            # Minimum length
            MinLengthValidator(
                3,
                message='Username must be at least 3 characters long.'),
            # Maximum length
            MaxLengthValidator(
                15,
                message='Username cannot be longer than 15 characters.'),
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'User Name',
                'aria-describedby': 'id_username_helptext'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            # Username field
            'username',
            # First name field
            'first_name',
            # Last name field
            'last_name',
            # Email field
            'email',
            # Password field (new password)
            'password1',
            # Password field (confirm password)
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the 'usable_password' field if it exists
        self.fields.pop('usable_password', None)

        # Configuration for the username field
        self.fields['username'].widget.attrs.update({
            # CSS class for styling
            'class': 'form-control',
            # Placeholder text
            'placeholder': 'User Name',
            # ARIA attribute for accessibility
            'aria-describedby': 'id_username_helptext'
        })
        # No label displayed
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<ul id="id_username_helptext" class="form-text text-muted">'
            '<li><small>3-15 characters. Letters, digits, and '
            '@/./+/-/_ only.</small></li>'
            '</ul>'
        )

        # Configuration for the password1 field
        self.fields['password1'].widget.attrs.update({
            # CSS class for styling
            'class': 'form-control',
            # Placeholder text
            'placeholder': 'Password',
            # ARIA attribute for accessibility
            'aria-describedby': 'id_password1_helptext'
        })
        # No label displayed
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul id="id_password1_helptext" '
            'class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal '
            'information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        # Configuration for the password2 field
        self.fields['password2'].widget.attrs.update({
            # CSS class for styling
            'class': 'form-control',
            # Placeholder text
            'placeholder': 'Confirm Password',
            # ARIA attribute for accessibility
            'aria-describedby': 'id_password2_helptext'
        })
        # No label displayed
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span id="id_password2_helptext" class="form-text text-muted">'
            '<small>Enter the same password as before, '
            'for verification.</small>'
            '</span>'
        )

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email) \
            .exclude(pk=self.instance.pk) \
                .exists():
            raise forms.ValidationError(
                'This email address is already in use.'
            )
        return email

    def clean_username(self):
        """Validate username uniqueness."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username) \
                .exclude(pk=self.instance.pk) \
                .exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )
        return username
