import json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
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
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

# Create your views here.

def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse('It works')

@csrf_exempt
def login_req(request: HttpRequest):
    """
    @param request: HttpRequest
    @return: HttpResponse
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    
    a = json.loads(request.body)
    print(a["phone"], a["taxi_licence"])

    csrf_token = get_token(request)

    return HttpResponse(csrf_token)
