# Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from datetime import timedelta, date
import json

def Search(request):
    a = 'hi'
    return render_to_response('index.html',a)

