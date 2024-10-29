from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index view
    path('ajax/load-options/', views.load_options, name='ajax_load_options'),  # AJAX URL for dropdown options
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Product detail view
]
