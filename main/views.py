from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Hotel, Restaurant, Reservation
from django.contrib import messages
from datetime import date
from .forms import CustomUserCreationForm

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
    # اگر فقط یک صفحهٔ جدا می‌خواهی که لینک به لاگین/ثبت‌نام باشد
    return render(request, 'login.html')


@login_required
def reserve_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    Reservation.objects.create(user=request.user, hotel=hotel, date=date.today())
    return redirect('main:panel')   # ← namespace اضافه شد


@login_required
def reserve_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    Reservation.objects.create(user=request.user, restaurant=restaurant, date=date.today())
    return redirect('main:panel')   # ← namespace اضافه شد


@login_required
def panel(request):
    reservation_count = Reservation.objects.filter(user=request.user).count()
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'panel.html', {
        'reservation_count': reservation_count,
        'reservations': reservations,
    })


# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.email = form.cleaned_data.get('email')
#             user.save()
#             login(request, user)  # بعد از ثبت‌نام کاربر وارد سیستم بشه
#             messages.success(request, 'ثبت‌نام با موفقیت انجام شد. خوش آمدید!')
#             return redirect('main:panel')  # به پنل کاربری منتقل بشه
#         else:
#             messages.error(request, 'ثبت‌نام ناموفق بود. لطفاً اطلاعات را بررسی کنید.')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'حساب شما با موفقیت ساخته شد.')
            return redirect('main:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'ورود با موفقیت انجام شد.')
            if user.is_staff:
                return redirect('admin:index') 
            else:
                return redirect('main:home') 
        else:
            messages.error(request, 'ورود ناموفق بود. لطفاً اطلاعات را بررسی کنید.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:home') 


@login_required
def dashboard(request):
    # اگر داشبورد جداگانه می‌خواهی، می‌توانی تمپلیت دیگر بدهی
    return render(request, 'panel.html')