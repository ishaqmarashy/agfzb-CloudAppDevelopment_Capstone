from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        next_url = request.GET.get('next', None)
        if not next_url:
            next_url=reverse('djangoapp:index')
        if user is not None:
            login(request, user)
            return redirect(f'{next_url}?success=True')
        else:
            return redirect(f'{next_url}?success=False')
        return render(request, request.path , context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "GET":
        return render(request,  'djangoapp/registration.html')
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['user']).exists():
            # User with this username already exists
            return redirect(f'/djangoapp/register?success=False')
        else:
            user = User.objects.create_user(username=request.POST['user'],
                                            password=request.POST['psw'],
                                            first_name=request.POST['firstname'],
                                            last_name=request.POST['lastname'])
            print(request.POST['user'], 'registered')
        return redirect(f'/djangoapp/register?success=True')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        return render(request, 'djangoapp/index.html', context)
