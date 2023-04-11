from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarModel

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
            User.objects.create_user(username=request.POST['user'],
                                     password=request.POST['psw'],
                                     first_name=request.POST['firstname'],
                                     last_name=request.POST['lastname'])
            print(request.POST['user'], 'registered')
        return redirect(f'/djangoapp/register?success=True')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request,**params):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/033a0f48-0899-4e67-9b85-b813b228e7c3/API/get-dealership"
        # Get dealers from the URL
        if 'dealer_id' in params:
            params['id'] = params['dealer_id']
            del params['dealer_id']
        dealerships = get_dealers_from_cf(url,**params)
        context['dealerships']=dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/033a0f48-0899-4e67-9b85-b813b228e7c3/API/review"
        # Get reviews from the URL
        params={'dealership':dealer_id}
        reviews = get_dealer_reviews_from_cf (url,**params)
        for review in reviews:
            print(f"Review ID: {str(review.id)}\nName: {review.name}\nSentiment: {review.sentiment}\n")
        context['reviews']=reviews
        context['id']=dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        context={'dealer_id':dealer_id}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/033a0f48-0899-4e67-9b85-b813b228e7c3/API/get-dealership"
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        context["dealer"] = get_dealer_by_id_from_cf(url, dealer_id)[0]
        context["now"]= datetime.utcnow().strftime('%Y-%m-%d')
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == "POST" and request.user.is_authenticated:
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/033a0f48-0899-4e67-9b85-b813b228e7c3/API/review"
        name = request.POST.get('name')
        purchase_check = request.POST.get('purchase_check')
        review = request.POST.get('review')
        purchase_date = request.POST.get('purchase_date')
        car = request.POST.get('car')
        if request.POST.get('purchase_check') is not None:
            car=car.split('***')
            car_make = car[0]
            car_model = car[1]
            car_year = car[2]
            purchase_check=True
        else:
            car_make = None
            car_model = None
            car_year = None
            purchase_check = False
        payload = {
        "review": {
            "dealership": dealer_id,
            "name": request.user.username,
            "purchase": purchase_check,
            "review": review,
            "purchase_date": purchase_date,
            "car_make": car_make,
            "car_model": car_model,
            "car_year": car_year,
            "sentiment": None
            }
        }
        response = post_request(url, payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    return redirect('djangoapp:index')
