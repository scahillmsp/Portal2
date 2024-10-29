from django.db import models
from django.contrib.auth.models import User

# Vehicle model, linked to Product via a ManyToMany relationship
class Vehicle(models.Model):
    category = models.CharField(max_length=100)  # e.g., Excavator, Bulldozer
    make = models.CharField(max_length=100)      # e.g., Caterpillar, Komatsu
    model = models.CharField(max_length=100)     # e.g., CAT 320D
    version = models.CharField(max_length=100, default="_")

    def __str__(self):
        return f"{self.category} {self.make} {self.model} {self.version}"

# Product model with a ManyToManyField to Vehicle
class Product(models.Model):
    part_number = models.CharField(max_length=255, unique=True, default="UNKNOWN")
    oem_number = models.CharField(max_length=255, blank=True, null=True)
    header = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    cross_reference_numbers = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    vehicles = models.ManyToManyField(Vehicle)  # Link products to multiple vehicles

    def __str__(self):
        return self.part_number

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  # Enforces uniqueness
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vat_exempt = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Order model for tracking customer orders
class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)  # An order can contain multiple products
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_number

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.id} for Order #{self.order.order_number}"