import json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
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
