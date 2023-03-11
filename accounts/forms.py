from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SipnUpForm(UserCreationForm):
    email = forms.CharField(max_length=300, widget=forms.EmailInput(), required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]