from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.management import call_command
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.views import generic

from datetime import datetime


from django.db.models import Q
from .forms import *
from .models import *



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
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  
            profile.save()
            return redirect('profile', pk=profile.pk)  
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'user/profile_form.html', {'form': form})



class ProfileDeleteView(generic.DeleteView):
    model = Profile
    template_name = 'profile_confirm_delete.html'
    success_url = reverse_lazy('home')

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
    template_name = 'sklad/sklad_list.html'
    

class SkladDetailView(generic.DetailView):
    model = Sklad
    template_name = 'sklad_detail.html'
    context_object_name = 'skld'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sklad = self.get_object()  # Get the current warehouse
        # Get products related to this warehouse
        context['products'] = SkladProduct.objects.filter(sklad=sklad, is_active=True)
        return context

    def get_queryset(self):
        # Ensure the user can only access their own warehouses
        return Sklad.objects.filter(user=self.request.user)


class SkladCreateView(generic.CreateView):
    model = Sklad
    fields = ['name', 'location']
    template_name = 'sklad/sklad_form.html'
    success_url = reverse_lazy('sklad-list')


class SkladUpdateView(generic.UpdateView):
    model = Sklad
    fields = ['name', 'location']
    template_name = 'sklad/sklad_form.html'
    success_url = reverse_lazy('sklad-list')


class SkladDeleteView(generic.DeleteView):
    model = Sklad
    template_name = 'sklad/sklad_confirm_delete.html'
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

        # Calculate the new balance based on the transaction type
        if transaction.transaction_type == 'debit':  # Assuming 'debit' means subtraction
            new_balance = client.balance - transaction.amount
            if new_balance < 0:
                messages.error(
                    self.request,
                    f'Transaction failed! The balance for {client.name} cannot go below zero.'
                )
                return self.form_invalid(form)
        elif transaction.transaction_type == 'credit':  # Assuming 'credit' means addition
            new_balance = client.balance + transaction.amount

        # Update the client's balance
        client.balance = new_balance
        client.save()

        transaction.save()

        # Send notification email
        subject = f'New Transaction for {client.name}'
        message = f'''Dear {client.name},

A new transaction has been processed on your account.

Transaction Details:
Type: {transaction.get_transaction_type_display()}
Amount: {transaction.amount}

Thank you for using our service.'''
        recipient = client.email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

        # Success message
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


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "orders/order_detail.html"

class OrderCreateView(generic.CreateView):
    model = Order
    template_name = "orders/order_form.html"
    fields = ["client", "product", "quantity", "price_at_purchase", "total_price", "status"]
    success_url = reverse_lazy("order-list")

class OrderUpdateView(generic.UpdateView):
    model = Order
    template_name = "orders/order_form.html"
    fields = ["client", "product", "quantity", "price_at_purchase", "total_price", "status"]
    success_url = reverse_lazy("order-list")

class OrderDeleteView(generic.DeleteView):
    model = Order
    template_name = "orders/order_conf_del.html"
    success_url = reverse_lazy("order-list")

# # Shop Part of the Project 

# class ShopHome(generic.TemplateView):
#     template_name = 'shop/shop_home.html'


class ShopProductListView(generic.ListView):
    model = ShopProduct
    template_name = 'shop/shop_home.html'
    context_object_name = 'products'

class ShopProductDetailView(generic.DetailView):
    model = ShopProduct
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class ShopProductCreateView(generic.CreateView):
    model = ShopProduct
    form_class = ShopProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop-home')


class ShopProductUpdateView(generic.UpdateView):
    model = ShopProduct
    form_class = ShopProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop-home')


class ShopProductDeleteView(generic.DeleteView):
    model = ShopProduct
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('shop-home')


# CartItem Views
class CartItemListView(generic.ListView):
    model = CartItem
    template_name = 'shop/cart.html'
    context_object_name = 'cart_items'


class CartItemCreateView(generic.CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'shop/cartitem_form.html'
    success_url = reverse_lazy('cartitem-list')

    def form_valid(self, form):
        # Decrease product stock when adding an item to the cart
        cart_item = form.save(commit=False)
        cart_item.product.stock -= cart_item.quantity
        if cart_item.product.stock < 0:
            return JsonResponse({"error": "Insufficient stock"}, status=400)
        cart_item.product.save()
        return super().form_valid(form)


class CartItemDeleteView(generic.DeleteView):
    model = CartItem
    template_name = 'shop/cartitem_confirm_delete.html'
    success_url = reverse_lazy('shop:cartitem-list')

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.product.stock += cart_item.quantity  # Restore stock on delete
        cart_item.product.save()
        return super().delete(request, *args, **kwargs)


class Cart(generic.TemplateView):
    template_name = 'shop/cart.html'

class Checkout(generic.TemplateView):
    template_name = 'shop/checkout.html'
    

def run_migrations(request):
    try:
        call_command('migrate', interactive=False)
        return JsonResponse({'status': 'success', 'message': 'Migrations completed successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})