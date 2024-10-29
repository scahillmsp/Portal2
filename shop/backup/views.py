from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Vehicle, Order, Customer
from django.contrib.auth.decorators import login_required

# Main index view for displaying search form and results
def index(request):
    categories = Vehicle.objects.values_list('category', flat=True).distinct()
    products = Product.objects.none()  # No products initially displayed

    category = request.GET.get('category')
    make = request.GET.get('make')
    model = request.GET.get('model')
    version = request.GET.get('version')
    query = request.GET.get('query', '').strip()

    if category or make or model or version or query:
        products = Product.objects.all()
        if category:
            products = products.filter(vehicles__category=category)
        if make:
            products = products.filter(vehicles__make=make)
        if model:
            products = products.filter(vehicles__model=model)
        if version:
            products = products.filter(vehicles__version=version)
        if query:
            products = products.filter(
                Q(part_number__icontains=query) |
                Q(description__icontains=query) |
                Q(oem_number__icontains=query)
            )
        products = products.distinct()

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
    })

# Load options for dynamic dropdown filtering
def load_options(request):
    category = request.GET.get('category')
    make = request.GET.get('make')
    model = request.GET.get('model')

    vehicles = Vehicle.objects.filter(category=category) if category else Vehicle.objects.all()
    if make:
        vehicles = vehicles.filter(make=make)
    if model:
        vehicles = vehicles.filter(model=model)

    makes = vehicles.values_list('make', flat=True).distinct()
    models = vehicles.values_list('model', flat=True).distinct()
    versions = vehicles.values_list('version', flat=True).distinct()

    data = {
        'makes': list(makes),
        'models': list(models),
        'versions': list(versions),
    }
    return JsonResponse(data)

# Product detail view with related parts
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_parts = Product.objects.filter(vehicles__in=product.vehicles.all()).exclude(id=product.id)[:5]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_parts': related_parts,
    })

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

# Cart view
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# Checkout view
@login_required
def checkout(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')
        products = Product.objects.filter(id__in=cart.keys())
        total_price = sum(product.price * cart[str(product.id)] for product in products)
        order = Order.objects.create(customer=customer, total_price=total_price)
        for product in products:
            order.products.add(product)
        order.save()
        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'shop/checkout.html')

# Order confirmation view
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    return render(request, 'shop/order_confirmation.html', {'order': order})

# Order history view
@login_required
def order_history(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})
