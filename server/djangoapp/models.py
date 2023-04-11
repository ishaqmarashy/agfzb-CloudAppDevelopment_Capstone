from django.db import models
from django.utils.timezone import now
from django.conf import settings


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"
    
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id=models.IntegerField()
    name = models.CharField(max_length=30)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    type = models.CharField(
        null=False,
        max_length=10,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField()
    def __str__(self):
        return f"Car Make: {self.car_make}, Name: {self.name}, Type: {self.type}, Year: {self.year}"

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip
        
    def __str__(self):
        return f"address: {self.address}, city: {self.city}, full_name: {self.full_name}, id: {self.id}, lat: {self.lat}, long: {self.long}, short_name: {self.short_name}, st: {self.st}, state: {self.state}, zip: {self.zip}"
    
class DealerReview :
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment 
        self.id=models.AutoField(primary_key=True)
    def __str__(self):
        return f"dealership: {self.dealership}, name: {self.name}, purchase: {self.purchase}, review: {self.review}, purchase_date: {self.purchase_date}, car_make: {self.car_make}, car_model: {self.car_model}, car_year: {self.car_year}, sentiment: {self.sentiment}, id: {self.id}"