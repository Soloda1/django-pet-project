from django.contrib.auth.views import *
from django.db.models import F, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from .models import *


class ProductsView(ListView):
    model = ProductProxy
    paginate_by = 15
    context_object_name = 'products'
    title_page = "Главная страница"

    def get_template_names(self):
        if self.request.htmx:
            return 'shop/components/product_list.html'
        return 'shop/products.html'


class ProductDetailView(DetailView):
    model = ProductProxy
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                messages.error(request, 'You have already made a review for this product.')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(rating=rating, content=content, created_by=request.user, product=product)
                else:
                    product.reviews.create(rating=rating, created_by=request.user, product=product)
        else:
            messages.error(request, 'You need to be logged in to make a review.')

        return redirect(request.path)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {'products': products, 'category': category}
    return render(request, 'shop/category_list.html', context)


def search_products(request):
    query = request.GET.get('q')
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    context = {'products': products}
    if not query or not products:
        return redirect('shop:products')
    return render(request, 'shop/products.html', context)

