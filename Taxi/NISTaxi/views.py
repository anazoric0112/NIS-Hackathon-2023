import math

import django.utils.timezone
from datetime import datetime, timedelta

from django.forms import Form
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpRequest
from django.template.context_processors import request

from .utils import *
from .models import *
from django.db.models import Q
from django.db.transaction import commit, rollback

# Create your views here.
def index(request):
    return HttpResponse("It works!")