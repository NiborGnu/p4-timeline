from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    usable_password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Username field configuration
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'User Name',
            'aria-describedby': 'id_username_helptext'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span id="id_username_helptext" class="form-text text-muted">'
            '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'
            '</span>'
        )
    
        # Password1 field configuration
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'aria-describedby': 'id_password1_helptext'
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul id="id_password1_helptext" class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )
    
        # Password2 field configuration
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'aria-describedby': 'id_password2_helptext'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span id="id_password2_helptext" class="form-text text-muted">'
            '<small>Enter the same password as before, for verification.</small>'
            '</span>'
    )

# Adding custom clean methods for email and username to ensure uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
