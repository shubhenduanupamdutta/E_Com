from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import stripe
from .models import Order, Product
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .send_mail import send_order_email
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


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
        queryset = Product.objects.filter(query).order_by('-id')

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
        if int(data['total_price']) == 0:
            messages.error(request, "Your cart is empty!")
            return redirect('index')
        order = Order(**data, payment_done=False)
        order.save()
        order.refresh_from_db()
        return redirect('stripe_checkout', order_id=order.id)  # type: ignore

    return render(request, 'shop/checkout.html')


class StripeCheckoutSession(View):
    """Stripe Checkout View"""

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        # print(order.id, order)
        order_detail = json.loads(order.items)
        order_name = ""
        for value in order_detail.values():
            order_name += f"{value[1]}: Qty: {value[0]} - {value[2]}\n"

        checkout_session = stripe.checkout.Session.create(
            currency="inr",
            payment_method_types=['card'],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": int(order.total_price * 100),  # type: ignore # noqa
                        "product_data": {
                            "name": order_name,
                        }
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "order_id": order_id,
                "order_details": order.items,
                "order_for": order.name,
            },
            mode="payment",
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        return redirect(checkout_session.url)


def success(request):
    messages.success(request, "Your order has been placed successfully!")
    return redirect('index')


def cancel(request):
    messages.error(request, "Your order has been cancelled!")
    return redirect('checkout')


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    Stripe Webhook View to handle checkout.session.completed event
    """

    def post(self, request, format=None):
        print("Webhook triggered")
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(  # type: ignore
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            print(e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:  # type: ignore
            # Invalid signature
            print(e)
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = int(session["metadata"]["order_id"])
            print(order_id)
            order = Order.objects.get(pk=order_id)
            order.payment_done = True
            order.save()
            order.refresh_from_db()
            print("Payment was successful.")
            print("calling send_order_email from webhook")
            send_order_email(order)
            print("Email Sent!")

        print("Just before HttpResponse")
        print(f"{event['type']}")
        msg = "production" if len(endpoint_secret) == 38 else "development"
        print(f"In {msg} mode")
        return HttpResponse(status=200)
