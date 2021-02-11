from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label="Haslo", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtorz haslo", strip=False, widget=forms.PasswordInput)
