from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.http import  HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


SYSTEM_NAME = 'RBMO Management System'
def home(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME}
    return render_to_response('home.html', data, context)

def logout_user(request):
    logout(request)
    data = {'system_name': SYSTEM_NAME}
    return HttpResponseRedirect('home')
    
