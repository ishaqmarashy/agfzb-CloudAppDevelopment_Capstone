from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
# - Name
    name= models.CharField(primary_key=True, max_length=30, default='Unspecified')
# - Description
    description= models.CharField(max_length=500, default='Unspecified')
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
    def __str__(self):
         return "Name: " + self.name + \
            +", Description: " + self.description + \
            + ", Make: " + self.car_make + \
            + ", Model: " + self.car_model + \
            + ", Year: " + self.car_year 
        
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make=models.ForeignKey(CarMake,on_delete=models.PROTECT)
# - Name
    name= models.CharField(max_length=30, default='Unspecified')
# - Dealer id, used to refer a dealer created in cloudant database.
    id= models.IntegerField(primary_key=True)
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    SEDAN='Sedan'
    SUV='SUV'
    WAGON='Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    type=models.CharField(
        null=False,
        max_length=10,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
# - Year (DateField)
    year= models.DateField()
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
    def __str__(self):
         return "Car Make: " + self.car_make + \
            +", Name: " + self.name + \
            + ", dealer: " + self.dealer + \
            + ", Type: " + self.type + \
            + ", Year: " + self.year 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    id=models.IntegerField(primary_key=True)
    city=models.CharField(max_length=50, default='Unspecified')
    state=models.CharField(max_length=50, default='Unspecified')
    st=models.CharField(max_length=50, default='Unspecified')
    address=models.CharField(max_length=50, default='Unspecified')
    zip=models.IntegerField(max_length=10)
    lat=models.FloatField()
    long=models.FloatField()
    short_name=models.CharField(max_length=50, default='Unspecified')
    full_name=models.CharField(max_length=100, default='Unspecified')
    def __str__(self):
        return "ID: " + self.id + \
        +", Name: " + self.city + \
        + ", State: " + self.state + \
        + ", Street: " + self.st + \
        + ", Address: " + self.address + \
        + ", ZIP: " + self.zip + \
        + ", Lat: " + self.lat + \
        + ", Long: " + self.long + \
        + ", Short Name: " + self.short_name + \
        + ", Full Name: " + self.full_name 

# <HINT> Create a plain Python class `DealerReview` to hold review data
class CarDealer(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50, default='Unspecified')
    dealership=models.IntegerField()
    review=models.CharField(max_length=500, default='Unspecified')
    purchase=models.BooleanField(default=False)
    purchase_date=models.DateField()
    car_make=models.ForeignKey(CarMake,on_delete=models.PROTECT)
    car_model=models.ForeignKey(CarModel,on_delete=models.PROTECT)
    def __str__(self):
          return "ID: " + self.id + \
        +", Name: " + self.city + \
        + ", Dealership: " + self.dealership + \
        + ", Review: " + self.review + \
        + ", Purchase: " + self.purchase + \
        + ", Purchase Date: " + self.purchase_date + \
        + ", Car Make: " + self.car_make + \
        + ", Car Model: " + self.car_model + \
        + ", Car Year: " + self.car_year 
