from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    average_price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # فقط برای رزرو هتل پر می‌شوند
    check_in  = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)

    # برای رزرو رستوران، می‌توانی مثلاً یک فیلد datetime (meal_time) داشته باشی
    reservation_date = models.DateField(null=True, blank=True)

    @property
    def nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0

    @property
    def unit_price(self):
        if isinstance(self.content_object, Hotel):
            return self.content_object.price_per_night
        if isinstance(self.content_object, Restaurant):
            return self.content_object.average_price
        return 0

    @property
    def total_price(self):
        if isinstance(self.content_object, Hotel):
            return self.nights * self.unit_price
        return self.unit_price        # برای رستوران فرضاً «میانگین قیمت یک وعده»
