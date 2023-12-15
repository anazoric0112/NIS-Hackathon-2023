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
from django.db.models import Max
import json

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
    
    user = None
    card = None
    try:
        user = User.objects.get(phone=a["phone"], taxilicence=a["taxilicence"])
        card = Card.objects.get(taxilicence=user.taxilicence)
    except (User.DoesNotExist, Card.DoesNotExist):
        if User.objects.filter(phone=a["phone"]).count() > 0:
            return HttpResponseForbidden("User with same phone exist, but licences doesn't match")
        if Card.objects.filter(taxilicence=a["taxilicence"]).count() > 0:
            return HttpResponseForbidden("User with same taxilicene exist, but phones doesn't match")
        user = User()
        card = Card()
        user.taxilicence = a["taxilicence"]
        user.phone = a["phone"]

        card.taxilicence = user
        tmp = Card.objects.aggregate(Max("number"))
        tmp = tmp['number__max']
        if tmp is None:
            tmp = 7824723600000000
        else:
            tmp = int(tmp)
        card.number = str(tmp + 1)
        card.discount = 0
        card.points = 0
        card.balance = 0

        user.save()
        card.save()
    
    
    csrf_token = get_token(request)
    ret = json.dumps({
        "csrftoken" : csrf_token,
        "number": card.number,
        "taxilicence": card.taxilicence.taxilicence,
        "discount": card.discount,
        "points": card.points,
        "balance": card.balance,
        "qrcode": card.qrcode,
    })
    return HttpResponse(ret)

    
