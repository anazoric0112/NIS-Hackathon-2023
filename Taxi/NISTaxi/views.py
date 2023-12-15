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
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_GET, require_POST
from django.middleware.csrf import get_token

from NISTaxi.qr.qr_utils import *

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
    user = json.loads(request.body)
    
    if User.objects.filter(phone=user["phone"], taxilicence=user["taxi_licence"]).exists():
        csrf_token = get_token(request)
        return HttpResponse(csrf_token)
    else:
        return HttpResponseForbidden()


#@csrf_protect
#@login_required
@require_GET
def get_qr_code(request: HttpRequest):
    taxi_licence = request.POST.get('taxi_licence')

    return HttpResponse(generate_qr_code_bytes(data='1'), content_type='application/octet-stream')

    
