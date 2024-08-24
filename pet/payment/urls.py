from django.urls import path

from .views import *
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-failed/', payment_failed, name='payment-failed'),
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order/', complete_order, name='complete-order'),
    path('webhook-stripe/', stripe_webhook, name='webhook-stripe'),
    # path('webhook-yookassa/', yookassa_webhook, name='webhook-yookassa'),
    path("order/<int:order_id>/pdf/", admin_order_pdf, name="admin_order_pdf"),
]