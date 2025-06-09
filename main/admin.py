from django.contrib import admin
from .models import Hotel, Restaurant, Reservation

admin.site.register(Hotel)
admin.site.register(Restaurant)
admin.site.register(Reservation)
