from django.urls import path
from .views import *

urlpatterns = [
    path('', ping),
    path('login', login_req),
    path('login/<str:ref_code>', login_referral, name='login_referral'),
    path('get_qr_code', get_qr_code),
    path('send_sms', send_sms_message),
    path('send_email', send_email_message),
    path('pump_attendant', pump_attendant, name='pump_attendant'),
    path('payment_to_the_card', payment_to_the_card, name='payment_to_the_card'),
]