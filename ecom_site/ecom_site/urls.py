"""
URL configuration for ecom_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path(
        'products/<int:pk>/',
        views.ProductDetail.as_view(),
        name='product_detail'
    ),
    path('stripe-checkout-session/<int:order_id>/',
         views.StripeCheckoutSession.as_view(), name="stripe_checkout"),
    path('register/', user_views.register, name="register"),
    path('login/', user_views.CustomLoginView.as_view(
        template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        template_name="users/logout.html"), name="logout"),
    path('checkout/', views.checkout, name="checkout"),
    path('admin/', admin.site.urls),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    path('stripe-webhook',
         views.StripeWebhookView.as_view(), name="webhook"),
]
