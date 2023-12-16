from django.urls import path
from .views import *

urlpatterns = [
    path('', ping),
    path('login', login_req),
    # path('get_qr_code', get_qr_code),
]