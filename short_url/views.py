from django.shortcuts import render
from django.http import request
from django.http import HttpResponse


def index(request):
    return HttpResponse("Teste de view")
