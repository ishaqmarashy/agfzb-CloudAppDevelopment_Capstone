from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview

# Register your models here.
admin.site.register(CarDealer)
admin.site.register(DealerReview)

# CarModelInline class
class CarModelInline (admin.TabularInline):
    extra = 1
    model = CarModel

# CarModelAdmin class
class CarModelAdmin (admin.ModelAdmin):
    list_display = ('name', 'car_make', 'year')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin (admin.ModelAdmin):
    inlines = [CarModelInline]
    readonly_fields=[]

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)
