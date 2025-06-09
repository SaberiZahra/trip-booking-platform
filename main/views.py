from django.shortcuts import render, redirect
from .models import Hotel, Restaurant, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date

def home(request):
    return render(request, 'home.html')

def hotels(request):
    q = request.GET.get('q')
    if q:
        hotels = Hotel.objects.filter(name__icontains=q)
    else:
        hotels = Hotel.objects.all()
    return render(request, 'hotels.html', {'hotels': hotels})

def restaurants(request):
    q = request.GET.get('q')
    if q:
        restaurants = Restaurant.objects.filter(name__icontains=q)
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'restaurants.html', {'restaurants': restaurants})


def login_register(request):
    return render(request, 'login.html')


@login_required
def reserve_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    Reservation.objects.create(user=request.user, hotel=hotel, date=date.today())
    return redirect('panel')

@login_required
def reserve_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    Reservation.objects.create(user=request.user, restaurant=restaurant, date=date.today())
    return redirect('my_panel')

@login_required
def panel(request):
    reservation_count = Reservation.objects.filter(user=request.user).count()
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'main/panel.html', {
        'reservation_count': reservation_count,
        'reservations': reservations,
    })

@login_required
def dashboard(request):
    return render(request, 'main/panel.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
