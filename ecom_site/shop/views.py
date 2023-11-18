from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView
# Create your views here.

class Index(ListView):
    model = Product
    template_name = "shop/index.html"
    context_object_name = "products"