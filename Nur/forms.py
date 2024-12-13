from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
# User
class UserSignupForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select a country")
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select a city")

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'country', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.cities.all()

class CustomUserForm(UserCreationForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select a country")
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select a city")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'country', 'city', 'address', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data

# Profile  
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user',  'bio', 'date_of_birth', 'profile_picture' ,'website']
        profile_picture = forms.URLField(required=False)
        website = forms.URLField(required=False)

from django import forms
from .models import Product

# Products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'index', 'price', 'cost_price', 'sold', 'category', 'colour', 'up_to', 'user']

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cost_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sold = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    up_to = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput(), required=False) 


# Transaction Form 
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['client', 'transaction_type', 'amount', 'comments']


