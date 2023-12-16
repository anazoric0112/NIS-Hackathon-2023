import json
import traceback
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import math
from django.shortcuts import redirect, render

import django.utils.timezone
from datetime import datetime, timedelta

from django.forms import Form
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpRequest
from django.template.context_processors import request

from .forms import *
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
from NISTaxi.referral.referral_utils import *

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
    
    #print(a, User.objects.filter(phone=a["phone"]).count(), Card.objects.filter(taxilicence=a["taxilicence"]).count())
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

@csrf_exempt
def login_referral(request, ref_code):
    if request.method != "POST":
        return HttpResponseBadRequest()
    
    referred_licence = decode_referral_code(ref_code)
    a = json.loads(request.body)
    user = None
    card = None
    referred_card = Card.objects.get(taxilicence=referred_licence)
    try:
        user = User.objects.get(phone=a["phone"], taxilicence=a["taxilicence"])
        card = Card.objects.get(taxilicence=user.taxilicence)
    except (User.DoesNotExist, Card.DoesNotExist):
        if User.objects.filter(phone=a["phone"]).count() > 0:
            return HttpResponseForbidden("User with same phone exist, but licences doesn't match")
        if Card.objects.filter(taxilicence=a["taxilicence"]).count() > 0:
            return HttpResponseForbidden("User with same taxilicene exist, but phones doesn't match")
        if Card.objects.filter(taxilicence=referred_licence).count() == 0:
            return HttpResponseForbidden("Invalid referral code")
        
        user = User()
        card = Card()
        user.taxilicence = a["taxilicence"]
        user.phone = a["phone"]
        if "email" in a:
            user.email = a["email"]

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
        referred_card.discount += 1
        referred_card.save()

        recom=Recomendation()
        user_who_referred = User.objects.get(taxilicence=referred_licence)
        recom.user1=user_who_referred
        recom.user2=user
        recom.save()


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

@csrf_exempt
@require_POST
def get_qr_code(request: HttpRequest):
    user_json = json.loads(request.body)
    print(user_json)
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

@csrf_exempt
@require_POST
def pump_attendant(request):

    try:
        pumpForm = pumpAttendantForm(request.POST)
        if pumpForm.is_valid():
            # Access the field value using the correct name
            card = Card.objects.get(number=pumpForm.cleaned_data['cardnumber'])

            if card is None:
                return HttpResponse(json.dumps({
                    "paid": 0,
                    "balance": 0,
                    "disc": False,
                    "points": False,
                    "msg": "Card doesn't exist"
                }), status=400);

            base_payment=pumpForm.cleaned_data['balance']
            discount=card.discount
            balance=card.balance
            points=card.points
            disc=False
            points=False

            if discount>0:
                discount-=1
                base_payment*=0.95
                disc=True

            if points>=100 and base_payment>=1000:
                points-=100
                base_payment-=1000
                points=True

            if balance>=base_payment:

                card.discount=discount
                card.points=points
                card.balance -= base_payment
                card.points+= int(base_payment/190)
                card.save()

                return HttpResponse(json.dumps({
                    "paid": base_payment,
                    "balance": card.balance,
                    "disc": disc,
                    "points": points,
                    "msg": "Success"
                }), status=200)
            else:
                return HttpResponse(json.dumps({
                    "paid": 0,
                    "balance": 0,
                    "disc": disc,
                    "points": points,
                    "msg": "Insufficient funds"
                }), status=400)
        else:
            return HttpResponseForbidden(json.dumps({
                    "paid": 0,
                    "balance": 0,
                    "disc": False,
                    "points": False,
                    "msg": "Error occured while processing the form"
                }), status=400)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return HttpResponseForbidden(json.dumps({
                    "paid": 0,
                    "balance": 0,
                    "disc": disc,
                    "points": points,
                    "msg": "Error occured while processing the form"
                }), status=400)

@csrf_exempt
@require_POST
def payment_to_the_card(request):
    try:
        pumpForm = pumpAttendantForm(request.POST)
        if pumpForm.is_valid():
            # Access the field value using the correct name
            card = Card.objects.get(number=pumpForm.cleaned_data['cardnumber'])

            if(card is not None):
                card.balance += pumpForm.cleaned_data['balance']
                card.save()

            return HttpResponse("Successfully deposited money") # Add the 'return' statement
        return HttpResponseForbidden("An error occurred while processing the form.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return HttpResponseForbidden("An error occurred while processing the form.")