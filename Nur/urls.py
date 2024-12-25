from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),
    path('dashboard',DashBoardView.as_view(),name='dashboard'),
    # Profile
    path('profile/create/', create_or_edit_profile, name='create-profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', create_or_edit_profile, name='update-profile'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='delete-profile'),

    # Product
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/update/<int:pk>/', product_update_view, name='product-update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),

    # Category
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),

    # Colour
    path('colours/', ColourListView.as_view(), name='colour-list'),
    path('colour/<int:pk>/', ColourDetailView.as_view(), name='colour-detail'),
    path('colour/create/', ColourCreateView.as_view(), name='colour-create'),
    path('colour/update/<int:pk>/', ColourUpdateView.as_view(), name='colour-update'),
    path('colour/delete/<int:pk>/', ColourDeleteView.as_view(), name='colour-delete'),

    # Sklad
    path('sklads/', SkladListView.as_view(), name='sklad-list'),
    path('sklad/<int:pk>/', SkladDetailView.as_view(), name='sklad-detail'),
    path('sklad/create/', SkladCreateView.as_view(), name='sklad-create'),
    path('sklad/update/<int:pk>/', SkladUpdateView.as_view(), name='sklad-update'),
    path('sklad/delete/<int:pk>/', SkladDeleteView.as_view(), name='sklad-delete'),

    # Sklad Product
    path('sklad-products/', SkladProductListView.as_view(), name='sklad-product-list'),
    path('sklad-product/<int:pk>/', SkladProductDetailView.as_view(), name='sklad-product-detail'),
    path('sklad-product/create/', SkladProductCreateView.as_view(), name='sklad-product-create'),
    path('sklad-product/update/<int:pk>/', SkladProductUpdateView.as_view(), name='sklad-product-update'),
    path('sklad-product/delete/<int:pk>/', SkladProductDeleteView.as_view(), name='sklad-product-delete'),
    
    # Clients
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    # Transactions for Clients 
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/<int:client_id>/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),

    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    path("orders/<int:pk>/edit/", OrderUpdateView.as_view(), name="order-edit"),
    path("orders/add/", OrderCreateView.as_view(), name="order-add"),
    # Shope Path's
    path('shop/',ShopProductListView.as_view(),name='shop-home'),
    path('cart/',CartItemListView.as_view(),name='cart'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    # For Server Render
    path('', run_migrations, name='run_migrations'),

]
