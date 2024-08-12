from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/<slug:category_slug>', category_list, name='category_list'),
    path("search_products/", search_products, name="search-products"),
]