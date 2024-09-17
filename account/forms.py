from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class SignUpForm(UserCreationForm):
    """
    Form for user registration including additional fields.
    """
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        )
    )
    first_name = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    username = forms.CharField(
        label='',
        max_length=15,
        min_length=3,
        validators=[
            MinLengthValidator(
                3,
                message='Username must be at least 3 characters long.'),
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
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, customize widgets and help texts.
        """
        super().__init__(*args, **kwargs)

        self.fields.pop('usable_password', None)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'User Name',
            'aria-describedby': 'id_username_helptext'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<ul id="id_username_helptext" class="form-text text-muted">'
            '<li><small>3-15 characters. Letters, digits, and '
            '@/./+/-/_ only.</small></li>'
            '</ul>'
        )

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'aria-describedby': 'id_password1_helptext'
        })
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

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'aria-describedby': 'id_password2_helptext'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span id="id_password2_helptext" class="form-text text-muted">'
            '<small>Enter the same password as before, '
            'for verification.</small>'
            '</span>'
        )

    def clean_email(self):
        """
        Validate that the email address is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email) \
            .exclude(pk=self.instance.pk) \
                .exists():
            raise forms.ValidationError(
                'This email address is already in use.'
            )
        return email

    def clean_username(self):
        """
        Validate that the username is unique.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username) \
                .exclude(pk=self.instance.pk) \
                .exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )
        return username
