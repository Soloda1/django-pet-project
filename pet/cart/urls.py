from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('add/', cart_add, name='add-to-cart'),
    # path('<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    # path('search/<slug:category_slug>', category_list, name='category_list'),
    # path("search_products/", search_products, name="search-products"),
]