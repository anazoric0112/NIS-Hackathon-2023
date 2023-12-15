<<<<<<< HEAD
from django.urls import path
from .views import *

urlpatterns = [
    path('', ping),
    path('login', login_req),
=======
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index')
>>>>>>> 4736802c0857e131c0fc329d18f8904b4accc328
]