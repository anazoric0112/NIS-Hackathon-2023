import json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
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
from django.db.models import Max
import json

from NISTaxi.qr.qr_utils import *
from NISTaxi.sms.sms_utils import *
from NISTaxi.email.email_utils import *

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
        card.qrcode = str(generate_qr_code_bytes(data = card.number))
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

    

@csrf_protect
@require_POST
def get_qr_code(request: HttpRequest):
    user_json = json.loads(request.body)
    try:
        card = Card.objects.get(taxilicence=user_json["taxilicence"])
        return HttpResponse(generate_qr_code_bytes(card.number))
        
    except (Card.DoesNotExist):
        return HttpResponseNotFound()

@csrf_exempt
def send_sms_message(request: HttpRequest):
    try:
        request_json = json.loads(request.body)

        msg = request_json["message"]

        send_sms(msg)

        return HttpResponse("Successfuly sent SMS message")
    except:
        return HttpResponseNotFound()
    
@csrf_exempt
def send_email_message(request: HttpRequest):
    try:
        request_json = json.loads(request.body)

        receiver_email = request_json['receiver_email']
        subject = request_json['subject']
        body = request_json['body']

        send_email(receiver_email, subject, body)

        return HttpResponse("Successfuly sent email message")
    except:
        return HttpResponseNotFound()