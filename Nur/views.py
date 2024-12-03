from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.db.models import Q
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
# Dashborad
@login_required
def dashboard(request):
    user = request.user
    profile = user.profile  
    profile_fields = ['bio', 'date_of_birth', 'profile_picture', 'website']
    
    completed_fields = sum([bool(getattr(profile, field)) for field in profile_fields])
    total_fields = len(profile_fields)
    profile_completion = (completed_fields / total_fields) * 100

    return render(request, 'dashboard.html', {
        'user': user,
        'profile_completion': round(profile_completion, 2),
        'profile': profile
    })
# Home
class HomeView(generic.TemplateView):
    template_name = 'main/home.html'

    def get_queryset(self):
        return Profile.objects.filter(active=True)
    
class DashBoardView(generic.TemplateView):
    template_name = 'main/dashboard.html'

# Profile
class ProfileCreateView(generic.CreateView):
    fields = ['bio','profile_picture','website','date_of_birth',]
    template_name = 'profile_form.html'
    success_url = reverse_lazy('home')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    benefit = (product.price - product.cost_price) * product.sold
    return render(request, 'product_detail.html', {'product': product, 'benefit': benefit})
class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        if created:
            return redirect(reverse_lazy('update-profile'))
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = context['profile'] 
        products = Product.objects.filter(user=self.request.user)  
        total_benefit = 0

        profile = context['profile']  
        products = Product.objects.filter(user=self.request.user) 
        total_benefit = 0
        for product in products:
            if product.sold > 0 and product.price: 
                total_benefit += (product.price - product.cost_price) * product.sold 

        context['total_benefit'] = total_benefit
        context['profile'] = profile 
        return context



        for product in products:
            if product.sold > 0 and product.price:  
                total_benefit += (product.price - product.cost_price) * product.sold 

        context['total_benefit'] = total_benefit
        context['profile'] = profile  
        return context
    
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
from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from .models import Product, Category

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user, is_active=True)
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(index__icontains=search_query)
            )

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        sort_by_date = self.request.GET.get('sort_by_date', '')
        if sort_by_date == 'asc':
            queryset = queryset.order_by('sold')  
        elif sort_by_date == 'desc':
            queryset = queryset.order_by('-sold')  

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() 
        return context

from django.shortcuts import render
from django.views import generic
from .models import Product

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']

        if product.sold > 0 and product.price and product.cost_price:
            profit_per_product = product.price - product.cost_price
            total_profit = profit_per_product * product.sold
        else:
            profit_per_product = 0
            total_profit = 0
        
        context['profit_per_product'] = profit_per_product
        context['total_profit'] = total_profit
        return context

@login_required 
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'product': product})


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

class ClientListView(generic.ListView):
    model = Client
    template_name = "clients/clients.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)
    
class ClientDetailView(generic.DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"
    
class ClientCreateView(generic.CreateView):
    model = Client
    template_name = "clients/client_form.html"
    fields = ['name', 'phone_number', 'email', 'address']
    success_url = reverse_lazy('client-list')

    def form_valid(self, form):
        form.instance.user = self.request.user 
        form.instance.balance = 0  
        return super().form_valid(form)
    
class ClientUpdateView(generic.UpdateView):
    model = Client
    template_name = "clients/client_form.html"
    fields = ['name', 'phone_number', 'email', 'address']
    success_url = reverse_lazy('client-list')

class ClientDeleteView(generic.DeleteView):
    model = Client
    template_name = "clients/conf_delete_client.html"
    success_url = reverse_lazy('client-list')