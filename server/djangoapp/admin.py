from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline (admin.TabularInline):
    extra = 1
    model = CarModel

# CarModelAdmin class
class CarModelAdmin (admin.ModelAdmin):
    list_display = ['name',  'dealer_id', 'type', 'year']
    search_fields = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin (admin.ModelAdmin):
    inlines = [CarModelInline]
    search_fields = ['name']

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake)
