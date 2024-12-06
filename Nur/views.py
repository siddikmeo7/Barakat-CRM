from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .forms import *
from .models import *
from django.db.models import Q


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'

    def get_queryset(self):
        return Profile.objects.filter(active=True)

class DashBoardView(generic.TemplateView):
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        products = Product.objects.filter(is_active=True, created_at__month=current_month, created_at__year=current_year)
        
        total_sold_products = products.aggregate(total_sold=Sum('sold'))['total_sold'] or 0
        
        profit_per_product = ExpressionWrapper(
            (F('price') - F('cost_price')) * F('sold'),
            output_field=DecimalField()
        )
        total_income = products.aggregate(total_income=Sum(profit_per_product))['total_income'] or 0
        
        total_benefit = products.aggregate(total_benefit=Sum((F('price') - F('cost_price')) * F('sold')))['total_benefit'] or 0
        
        total_products_in_stock = products.aggregate(total_stock=Sum(F('up_to') - F('sold')))['total_stock'] or 0
        
        out_of_stock_products = products.filter(up_to=0).count()
        
        total_clients = Client.objects.count()

        context['total_products_in_stock'] = total_products_in_stock
        context['out_of_stock_products'] = out_of_stock_products
        context['total_clients'] = total_clients
        context['total_income'] = total_income
        context['total_sold_products'] = total_sold_products
        context['total_benefit'] = total_benefit

        return context

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile'] 
        products = Product.objects.filter(user=self.request.user)  
        total_benefit = 0

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

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        
        if hasattr(product, 'cost_price'):
            benefit = (product.sold - product.price) 
        else:
            benefit = 0
        
        context['benefit'] = benefit
        return context


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')  

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST' or request.POST.get('_method') == 'PUT': 
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list') 
        else:
            return render(request, 'products/product_form.html', {'form': form, 'product': product})
    
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
    template_name = 'skladproduct/sklad_product_list.html'
    context_object_name = 'sklad_products'


class SkladProductDetailView(generic.DetailView):
    model = SkladProduct
    template_name = 'skladproduct/sklad_product_detail.html'
    context_object_name = 'sklad_product'


class SkladProductCreateView(generic.CreateView):
    model = SkladProduct
    fields = ['sklad', 'product', 'quantity']
    template_name = 'skladproduct/sklad_product_form.html'
    success_url = reverse_lazy('sklad-product-list')


class SkladProductUpdateView(generic.UpdateView):
    model = SkladProduct
    fields = ['sklad', 'product', 'quantity']
    template_name = 'skladproduct/sklad_product_form.html'
    success_url = reverse_lazy('sklad-product-list')


class SkladProductDeleteView(generic.DeleteView):
    model = SkladProduct
    template_name = 'skladproduct/sklad_product_conf_delete.html'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['transactions'] = client.transaction_set.all()
        return context

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

# Transaction Part for Client
class TransactionListView(generic.ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(client__user=self.request.user)

class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'

class TransactionCreateView(generic.CreateView):
    model = Transaction
    fields = ['transaction_type', 'amount', 'comments']
    template_name = 'transaction/transaction_form.html'

    def form_valid(self, form):
        client = get_object_or_404(Client, pk=self.kwargs['client_id'])
        transaction = form.save(commit=False)
        transaction.client = client
        transaction.user = self.request.user

        transaction.save() 

        subject = f'New Transaction for {client.name}'
        message = f'Dear {client.name},\n\nA new transaction has been processed on your account.\n\nTransaction Details:\nType: {transaction.get_transaction_type_display()}\nAmount: {transaction.amount}\n\nThank you for using our service.'
        recipient = client.email

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

        messages.success(self.request, f'Transaction for {client.name} successfully created!')
        return redirect('client-detail', pk=client.id)


    
class TransactionUpdateView(generic.UpdateView):
    model = Transaction
    template_name = 'transactions/transaction_form.html'
    form_class = TransactionForm

    def get_success_url(self):
        return reverse_lazy('transaction-list')


class TransactionDeleteView(generic.DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')