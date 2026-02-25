from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product


def shop(request):
    products = Product.objects.all().order_by('-created_at')
    category_key = request.GET.get('c') or ''
    query = (request.GET.get('q') or '').strip()

    if category_key:
        products = products.filter(category=category_key)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    categories = Product.CATEGORY_CHOICES
    context = {
        "products": products,
        "active_category": category_key,
        "query": query,
        "categories": categories,
    }
    return render(request, 'shop.html', context)


def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {"product": product})

# Create your views here.
