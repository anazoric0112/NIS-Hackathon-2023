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

from .sms.sms_utils import send_sms
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
    
    print(a)
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
        if a["email"]!="":
            user.email=a["email"]

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
        print(msg)
        send_sms(msg)

        return HttpResponse("Successfuly sent SMS message")
    except Exception as e:
        print(e)
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
        requestjson=json.loads(request.body)
        # Access the field value using the correct name
        card = Card.objects.get(number=requestjson['cardnumber'])

        if card is None:
            return HttpResponse(json.dumps({
                "paid": 0,
                "balance": 0,
                "disc": False,
                "points": False,
                "msg": "Card doesn't exist"
            }), status=200);

        base_payment=int(requestjson['balance'])
        og_payment=base_payment
        discount=card.discount
        balance=card.balance
        points=card.points
        disc=False
        pts=False

        if discount>0:
            discount-=1
            base_payment*=0.95
            disc=True

        if points>=100 and base_payment>=1000:
            points-=100
            base_payment-=1000
            pts=True

        if balance>=base_payment:

            card.discount=discount
            card.points=points
            card.balance -= base_payment
            card.points+= int(base_payment/190)
            card.save()
            print(base_payment)
            print(og_payment)

            email=card.taxilicence.email
            if email!=None and email!="":
                subject = "Transaction info"
                body = "Payment processed.\n"+\
                       "Total sum: "+str(base_payment)+"din.\n"+ \
                        "Points used: "+str(100 if pts else 0)+".\n"+ \
                        "Discount used: "+str("5%" if disc else "none")+".\n\n"+\
                            "Current balance: "+str(card.balance)+"din\n."

                send_email(email, subject, body)


            return HttpResponse(json.dumps({
                "paid": base_payment,
                "balance": og_payment,
                "disc": disc,
                "points": pts,
                "msg": "Success"
            }), status=200)
        else:
            return HttpResponse(json.dumps({
                "paid": 0,
                "balance": 0,
                "disc": False,
                "points": False,
                "msg": "Insufficient funds"
            }), status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return HttpResponseForbidden(json.dumps({
                    "paid": 0,
                    "balance": 0,
                    "disc": False,
                    "points": False,
                    "msg": "Error occured while processing the form"
                }), status=400)

@csrf_exempt
@require_POST
def payment_to_the_card(request):
    try:
            # Access the field value using the correct name
            requestjson=json.loads(request.body)
            card = Card.objects.get(number=requestjson['cardnumber'])

            if(card is not None):
                card.balance += requestjson['balance']
                card.save()

                email = card.taxilicence.email
                if email != None and email != "":
                    subject = "Transaction info"
                    body = "Payment processed.\n"+\
                           "Total sum added to the card: "+str(requestjson['balance'])+"din.\n\n"+\
                            "Current balance: "+str(card.balance)+"din\n."

                    send_email(email, subject, body)

            return HttpResponse("Successfully deposited money")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return HttpResponseForbidden("An error occurred while processing the form.")

@csrf_exempt
def get_card(request,id):
    card=Card.objects.get(number=id)
    return HttpResponse(json.dumps({
        "number": card.number,
        "taxiLicence": card.taxilicence.taxilicence,
        "discount": card.discount,
        "points": card.points,
        "balance": card.balance,
        "qrcode": card.qrcode,
    }))