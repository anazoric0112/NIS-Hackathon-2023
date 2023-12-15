from django.urls import path
from .views import *

urlpatterns = [
    path('', ping),
    path('login', login_req),
]