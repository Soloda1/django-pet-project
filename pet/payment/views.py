import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse

from cart.cart import Cart
from .forms import *
from .models import *

@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')
    else:
        return render(request, 'shipping/shipping.html', {'form': form})


def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')


def checkout(request):
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.get(user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})

    else:
        return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user,
        defaults={
            'full_name': name,
            'email': email,
            'street_address': street_address,
            'city': city,
            'apartment_address': apartment_address,
            'country': country,
            'zip_code': zip_code,
        })

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
        else:
            order = Order.objects.create(shipping_address=shipping_address, amount=total_price)

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'])

        return JsonResponse({'status': 'success'})
    else:
        return redirect('payment:checkout')