from django.db import models
from django.utils.timezone import now
from django.conf import settings


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

class CarDealer(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    st = models.CharField(max_length=50,blank=True)
    address = models.CharField(max_length=50,blank=True)
    zip = models.IntegerField(blank=True)
    lat = models.FloatField(blank=True)
    long = models.FloatField(blank=True)
    short_name = models.CharField(max_length=50,blank=True)
    full_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"ID: {self.id}, Name: {self.city}, State: {self.state}, Street: {self.st}, Address: {self.address}, ZIP: {self.zip}, Lat: {self.lat}, Long: {self.long}, Short Name: {self.short_name}, Full Name: {self.full_name}"

class CarModel(models.Model):
    id =  models.AutoField(primary_key=True)
    year = models.DateField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealerid=models.ForeignKey(CarDealer, on_delete=models.CASCADE)
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
    
    def __str__(self):
        return f"Car Make: {self.car_make}, Name: {self.name}, Type: {self.type}, Year: {self.year}"


class DealerReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    publish = models.DateField(auto_now_add=True)
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(default=now)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Dealership: {self.dealership}, Review: {self.review}, Purchase: {self.purchase}, Purchase Date: {self.purchase_date}, Car Make: {self.car_make}, Car Model: {self.car_model}, Car Year: {self.car_model.year}"
