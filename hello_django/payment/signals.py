from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED,ST_PP_PENDING
from paypal.standard.ipn.signals import valid_ipn_received
import weasyprint
from io import BytesIO
from order.models import Order
from django.dispatch import Signal,receiver

#@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # payment was successful
        print('*******************Got the signal ******************************')
        order = get_object_or_404(Order, id=ipn_obj.invoice)

        # mark the order as paid
        order.paid = True
        order.save()

        # create invoice e-mail
        subject = 'My Shop - Invoice nr. {}'.format(order.id)
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

        # generate PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()  #将内存中数据存入out
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + './css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
        # attach PDF file
        email.attach('order_{}.pdf'.format(order.id),out.getvalue(),'application/pdf')
        # send e-mail
        email.send()

valid_ipn_received.connect(payment_notification)
