
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Vehicle, Order, Customer
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Invoice
import uuid

def generate_unique_order_number():
    while True:
        order_number = str(uuid.uuid4())
        if not Order.objects.filter(order_number=order_number).exists():
            return order_number

@login_required
def index(request):
    customer = Customer.objects.get(user=request.user)
    categories = Vehicle.objects.values_list('category', flat=True).distinct()
    products = Product.objects.none()

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
        'customer_name': customer.name,
    })

@login_required
def place_order(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('cart')

        products = Product.objects.filter(id__in=cart.keys())
        total_price = sum(product.price * cart[str(product.id)] for product in products)
        order_number = generate_unique_order_number()

        order = Order.objects.create(customer=customer, total_price=total_price, order_number=order_number)
        for product in products:
            order.products.add(product)

        order.save()
        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)

    return redirect('cart')

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

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_parts = Product.objects.filter(vehicles__in=product.vehicles.all()).exclude(id=product.id)[:5]
    customer = Customer.objects.get(user=request.user)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_parts': related_parts,
        'customer_name': customer.name,
    })

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    customer = Customer.objects.get(user=request.user)
    vat_rate = Decimal('0.23') if not customer.vat_exempt else Decimal('0')

    cart_items = []
    total_price = Decimal('0.00')
    for product in products:
        quantity = cart[str(product.id)]
        product_price = product.price * (1 + vat_rate)
        total_price += product_price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'price_with_vat': product_price})

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'customer_name': customer.name,
    })

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)

        request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')
        products = Product.objects.filter(id__in=cart.keys())
        total_price = sum(product.price * cart[str(product.id)] for product in products)
        order_number = generate_unique_order_number()
        order = Order.objects.create(customer=customer, total_price=total_price, order_number=order_number)
        for product in products:
            order.products.add(product)
        order.save()
        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'shop/checkout.html', {'customer_name': customer.name})

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    return render(request, 'shop/order_confirmation.html', {'order': order, 'customer_name': order.customer.name})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_at')
    customer = Customer.objects.get(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders, 'customer_name': customer.name})

def invoice_view(request, order_id):
    invoice = get_object_or_404(Invoice, order__id=order_id)
    customer = Customer.objects.get(user=request.user)
    return render(request, 'shop/invoice.html', {'invoice': invoice, 'customer_name': customer.name})
