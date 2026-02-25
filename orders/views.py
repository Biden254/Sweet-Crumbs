import random
import string
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from products.models import Product
from .models import Order, OrderItem


def _get_cart(session):
    return session.setdefault('cart', {})


def cart_view(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal('0.00')
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        line_total = product.price * int(qty)
        items.append({"product": product, "quantity": int(qty), "line_total": line_total})
        total += line_total
    return render(request, 'cart.html', {"items": items, "total": total})


def add_to_cart(request, product_id: int):
    cart = _get_cart(request.session)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, product_id: int):
    cart = _get_cart(request.session)
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session.modified = True
    return redirect('cart')


def _generate_order_id() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def checkout(request):
    cart = _get_cart(request.session)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        delivery_date = request.POST.get('delivery_date')

        total = Decimal('0.00')
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, pk=int(product_id))
            total += product.price * int(qty)

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_id=_generate_order_id(),
            total_price=total,
            status='pending',
            name=name,
            email=email,
            phone=phone,
            address=address,
            delivery_date=delivery_date,
        )
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, pk=int(product_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(qty),
                price=product.price,
            )

        # Send confirmation email
        send_mail(
            subject=f"Order {order.order_id} Confirmation",
            message=f"Thank you for your order! Total: ${order.total_price}.",
            from_email=None,
            recipient_list=[email],
        )

        # clear cart
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success', order_id=order.order_id)

    # GET -> show checkout form
    items = []
    total = Decimal('0.00')
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        line_total = product.price * int(qty)
        items.append({"product": product, "quantity": int(qty), "line_total": line_total})
        total += line_total
    return render(request, 'checkout.html', {"items": items, "total": total})


def order_success(request, order_id: str):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order_success.html', {"order": order})


def track_order(request):
    order = None
    query = request.GET.get('order_id')
    if query:
        order = Order.objects.filter(order_id=query).first()
    return render(request, 'track_order.html', {"order": order})

# Create your views here.
