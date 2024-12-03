from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import generic
from django.urls import reverse_lazy
from .forms import *
from .models import *


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'

    def get_queryset(self):
        return Profile.objects.filter(active=True)
    
class DashBoardView(generic.TemplateView):
    template_name = 'main/dashboard.html'

    
class ProfileCreateView(generic.CreateView):
    fields = ['bio','profile_picture','website','date_of_birth',]
    template_name = 'profile_form.html'
    success_url = reverse_lazy('home')


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        if created:
            return redirect(reverse_lazy('update-profile'))
        return profile
    

def create_or_edit_profile(request, pk=None):
    if pk:
        profile = get_object_or_404(Profile, pk=pk, user=request.user)
    else:
        profile = None

    if request.method == 'POST':
        if profile:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.profile.pk)  
    else:
        form = ProfileForm(instance=profile) if profile else ProfileForm()
    return render(request, 'user/profile_form.html', {'form': form})


class ProfileDeleteView(generic.DeleteView):
    model = Profile
    template_name = 'profile_confirm_delete.html'
    success_url = reverse_lazy('home')


# Country Views
class CountryListView(generic.ListView):
    model = Country
    template_name = 'country_list.html'
    context_object_name = 'countries'


class CountryDetailView(generic.DetailView):
    model = Country
    template_name = 'country_detail.html'
    context_object_name = 'country'


class CountryCreateView(generic.CreateView):
    model = Country
    fields = ['name']
    template_name = 'country_form.html'
    success_url = reverse_lazy('country-list')


class CountryUpdateView(generic.UpdateView):
    model = Country
    fields = ['name']
    template_name = 'country_form.html'
    success_url = reverse_lazy('country-list')


class CountryDeleteView(generic.DeleteView):
    model = Country
    template_name = 'country_confirm_delete.html'
    success_url = reverse_lazy('country-list')


# City Views
class CityListView(generic.ListView):
    model = City
    template_name = 'city_list.html'
    context_object_name = 'cities'


class CityDetailView(generic.DetailView):
    model = City
    template_name = 'city_detail.html'
    context_object_name = 'city'


class CityCreateView(generic.CreateView):
    model = City
    fields = ['name', 'country']
    template_name = 'city_form.html'
    success_url = reverse_lazy('city-list')


class CityUpdateView(generic.UpdateView):
    model = City
    fields = ['name', 'country']
    template_name = 'city_form.html'
    success_url = reverse_lazy('city-list')


class CityDeleteView(generic.DeleteView):
    model = City
    template_name = 'city_confirm_delete.html'
    success_url = reverse_lazy('city-list')


# Product Views
class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/products.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user, is_active=True)

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list') 
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


class ProductUpdateView(generic.UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'colour']
    template_name = 'product_form.html'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(generic.DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')


# Category Views
class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Colour Views
class ColourListView(generic.ListView):
    model = Colour
    template_name = 'colour_list.html'
    context_object_name = 'colours'


class ColourDetailView(generic.DateDetailView):
    model = Colour
    template_name = 'colour_detail.html'
    context_object_name = 'colour'


class ColourCreateView(generic.CreateView):
    model = Colour
    fields = ['name']
    template_name = 'colour_form.html'
    success_url = reverse_lazy('colour-list')


class ColourUpdateView(generic.UpdateView):
    model = Colour
    fields = ['name']
    template_name = 'colour_form.html'
    success_url = reverse_lazy('colour-list')


class ColourDeleteView(generic.DeleteView):
    model = Colour
    template_name = 'colour_confirm_delete.html'
    success_url = reverse_lazy('colour-list')


# Sklad Views
class SkladListView(generic.ListView):
    model = Sklad
    template_name = 'sklad_list.html'
    context_object_name = 'sklads'


class SkladDetailView(generic.DetailView):
    model = Sklad
    template_name = 'sklad_detail.html'
    context_object_name = 'sklad'


class SkladCreateView(generic.CreateView):
    model = Sklad
    fields = ['name', 'location']
    template_name = 'sklad_form.html'
    success_url = reverse_lazy('sklad-list')


class SkladUpdateView(generic.UpdateView):
    model = Sklad
    fields = ['name', 'location']
    template_name = 'sklad_form.html'
    success_url = reverse_lazy('sklad-list')


class SkladDeleteView(generic.DeleteView):
    model = Sklad
    template_name = 'sklad_confirm_delete.html'
    success_url = reverse_lazy('sklad-list')


# SkladProduct Views
class SkladProductListView(generic.ListView):
    model = SkladProduct
    template_name = 'sklad_product_list.html'
    context_object_name = 'sklad_products'


class SkladProductDetailView(generic.DetailView):
    model = SkladProduct
    template_name = 'sklad_product_detail.html'
    context_object_name = 'sklad_product'


class SkladProductCreateView(generic.CreateView):
    model = SkladProduct
    fields = ['sklad', 'product', 'quantity']
    template_name = 'sklad_product_form.html'
    success_url = reverse_lazy('sklad-product-list')


class SkladProductUpdateView(generic.UpdateView):
    model = SkladProduct
    fields = ['sklad', 'product', 'quantity']
    template_name = 'sklad_product_form.html'
    success_url = reverse_lazy('sklad-product-list')


class SkladProductDeleteView(generic.DeleteView):
    model = SkladProduct
    template_name = 'sklad_product_confirm_delete.html'
    success_url = reverse_lazy('sklad-product-list')