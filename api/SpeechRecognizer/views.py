
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render 
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def index(request):
     return render(request, 'home.html')

def start(request):
	return render(request, 'home.html')