from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'country', 'city',  'region', 'address', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data

    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'date_of_birth', 'profile_picture']