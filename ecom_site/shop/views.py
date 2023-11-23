from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Order, Product
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


class Index(ListView):
    model = Product
    template_name = "shop/index.html"
    # context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        # Retrieve the search parameter from the request
        search_param = self.request.GET.get('item_name', '')

        # Apply filtering based on the search parameter
        query = Q(title__icontains=search_param)
        query = query | Q(category__icontains=search_param)
        query = query | Q(description__icontains=search_param)
        queryset = Product.objects.filter(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the search parameter to the context for use in the template
        context['search_param'] = self.request.GET.get('item_name', '')
        context['products_page'] = context.pop('page_obj')

        return context


class ProductDetail(DetailView):
    model = Product


@login_required
def checkout(request):

    if request.method == "POST":
        fields = ['items', 'name', 'email',
                  'address', 'city', 'state', 'zip_code', 'total_price']
        data = {field: request.POST.get(field, "") for field in fields}

        order = Order(**data)
        order.save()
        messages.success(request, "Order placed successfully!")
        return redirect('index')

    return render(request, 'shop/checkout.html')
