from django import forms
from .models import Reservation
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class HotelReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = ["check_in", "check_out"]
        widgets = {
            "check_in":  forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        c_in, c_out = cleaned.get("check_in"), cleaned.get("check_out")
        if c_in and c_out and c_out <= c_in:
            raise forms.ValidationError("تاریخ خروج باید بعد از ورود باشد.")
        return cleaned


class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date']  # فقط تاریخ رزرو رو می‌گیریم
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_reservation_date(self):
        date = self.cleaned_data.get('reservation_date')
        if date and date < date.today():
            raise forms.ValidationError("تاریخ رزرو نمی‌تواند قبل از امروز باشد.")
        return date
