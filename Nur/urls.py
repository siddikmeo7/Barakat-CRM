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

    # Country
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path('country/create/', CountryCreateView.as_view(), name='country-create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country-update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country-delete'),

    # City
    path('cities/', CityListView.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
    path('city/create/', CityCreateView.as_view(), name='city-create'),
    path('city/update/<int:pk>/', CityUpdateView.as_view(), name='city-update'),
    path('city/delete/<int:pk>/', CityDeleteView.as_view(), name='city-delete'),

    # Product
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', product_create, name='product-create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
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
]
