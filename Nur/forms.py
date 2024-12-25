from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
# User
class UserSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'password1', 'password2']

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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['website'].required = False  # Make website optional


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

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['client', 'transaction_type', 'amount', 'comments']


class ShopCategoryForm(forms.ModelForm):
    class Meta:
        model = ShopCategory
        fields = ['name', 'is_active']


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['name', 'category', 'description', 'price', 'stock', 'image', 'is_active']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'is_active']


