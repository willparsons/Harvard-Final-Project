from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "chat/layout.html")


def groups(request):
    return render(request, "chat/layout.html")


def friends(request):
    return render(request, "chat/layout.html")
