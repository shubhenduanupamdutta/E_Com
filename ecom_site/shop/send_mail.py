from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Order
import json


def send_order_email(order: Order):
    print("Creating mail to customer and vendor")
    # Email to customer
    subject_c = "Thank you for your purchase!"
    message_c = f"Hi {order.name},\n\n"
    message_c += "We appreciate your business!\n\n"
    message_c += "Your order:\n"
    for value in json.loads(order.items).values():
        message_c += f"{value[1]}: Qty: {value[0]} - {value[2]}\n"
    message_c += f"Total Price: {order.total_price}\n\n"
    message_c += "Thanks again for your purchase!\n"
    message_c += "The Ecom Site Team"
    mail_to_c = [order.email]
    print("Mail to customer created")

    from_mail = settings.EMAIL_HOST_USER

    # Email to vendor
    print("Creating mail to vendor")
    subject_v = "New Order Received!"
    message_v = "Hi Shubhendu,\n\n"
    message_v += "You have received a new order!\n\n"
    message_v += "Order Details:\n"
    for key, value in json.loads(order.items).items():
        message_v += (
            f"Product ID: {key} - {value[1]}: Qty: {value[0]} - {value[2]}\n"
        )
    message_v += f"Total Price: {order.total_price}\n\n"
    message_v += "Payment done in full"
    address = f"{order.address}, {order.city}, {order.state}, {order.zip_code}"
    message_v += f"\nShipping Address: {address}\n\n"
    mail_to_v = [settings.VENDOR_EMAIL]
    print("Mail to vendor created")

    message1 = (
        subject_c,
        message_c,
        from_mail,
        mail_to_c,
    )
    message2 = (
        subject_v,
        message_v,
        from_mail,
        mail_to_v,
    )
    # Sending mails using send_mass_mail()
    print("Sending mails using mass mail")
    send_mass_mail((message1, message2), fail_silently=False)  # type: ignore
