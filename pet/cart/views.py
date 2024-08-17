from decimal import Decimal
from itertools import product

from django.contrib.auth.views import *
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from django.http import JsonResponse

from shop.models import ProductProxy

from .cart import Cart


def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart-view.html', context=context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = ProductProxy.objects.get(pk=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_qty = len(cart)

        response = JsonResponse(data={'qty': cart_qty, 'product': str(product.title)})

        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id=product_id)
        cart_qty = len(cart)
        cart_total = cart.get_total_price()

        return JsonResponse({'qty': cart_qty, 'total': cart_total})


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product_id=product_id, quantity=product_qty)

        cart_qty = len(cart)
        cart_total = cart.get_total_price()

        return JsonResponse({'qty': cart_qty, 'total': cart_total})