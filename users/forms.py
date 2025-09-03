from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Extended user registration form
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    telegram_username = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telegram username (without @)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'telegram_username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.telegram_username = self.cleaned_data['telegram_username']
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    """
    User profile update form
    """
    password = None  # Remove password field

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'telegram_username')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telegram username (without @)'
            }),
        }