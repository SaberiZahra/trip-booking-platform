from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from .models import Hotel, Restaurant, Reservation
from .forms import CustomUserCreationForm, HotelReservationForm, RestaurantReservationForm


def home(request):
    return render(request, 'home.html')


def login_register(request):
    return render(request, 'login.html')


def hotels(request):
    q = request.GET.get('q')
    if q:
        hotels = Hotel.objects.filter(name__icontains=q)
    else:
        hotels = Hotel.objects.all()
    return render(request, 'hotels.html', {'hotels': hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    form  = HotelReservationForm()
    return render(request, "detail/hotel_detail.html",
                  {"hotel": hotel, "form": form})


@login_required
def create_hotel_reservation(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == "POST":
        form = HotelReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.content_object = hotel
            res.save()
            return redirect("main:panel")
    return redirect("main:hotel_detail", pk=pk)


@login_required
def reserve_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    
    if request.method == "POST":
        form = HotelReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.content_object = hotel
            res.save()
            messages.success(request, "رزرو شما ثبت شد.")
            return redirect("main:panel")
    else:
        form = HotelReservationForm()
    
    return render(request, "main/reserve_hotel.html", {"form": form, "hotel": hotel})



def restaurants(request):
    q = request.GET.get('q')
    if q:
        restaurants = Restaurant.objects.filter(name__icontains=q)
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'restaurants.html', {'restaurants': restaurants})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantReservationForm()
    return render(request, "detail/restaurant_detail.html",
                  {"restaurant": restaurant, "form": form})


@login_required
def create_restaurant_reservation(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == "POST":
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():      # همیشه True چون فیلدی ندارد
            res = form.save(commit=False)
            res.user = request.user
            res.content_object = restaurant
            res.save()
            return redirect("main:panel")
    return redirect("main:restaurant_detail", pk=pk)


@login_required
def reserve_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    content_type = ContentType.objects.get_for_model(Restaurant)

    if request.method == "POST":
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.content_type = content_type
            reservation.object_id = restaurant.id
            reservation.created_at = timezone.now()  # زمان ثبت رزرو
            reservation.save()
            messages.success(request, "رزرو رستوران با موفقیت ثبت شد.")
            return redirect('main:panel')
    else:
        form = RestaurantReservationForm()

    return render(request, 'detail/reserve_restaurant.html', {'restaurant': restaurant, 'form': form})


# @login_required
# def reserve_hotel(request, hotel_id):
#     hotel = Hotel.objects.get(id=hotel_id)
#     Reservation.objects.create(user=request.user, hotel=hotel, date=date.today())
#     return redirect('main:panel')   # ← namespace اضافه شد


# @login_required
# def reserve_restaurant(request, restaurant_id):
#     restaurant = Restaurant.objects.get(id=restaurant_id)
#     Reservation.objects.create(user=request.user, restaurant=restaurant, date=date.today())
#     return redirect('main:panel')   # ← namespace اضافه شد


@login_required
def panel(request):
    all_reservations = Reservation.objects.filter(user=request.user).select_related('content_type')

    hotel_ct  = ContentType.objects.get_for_model(Hotel)
    rest_ct   = ContentType.objects.get_for_model(Restaurant)

    hotel_reservations = all_reservations.filter(content_type=hotel_ct)
    restaurant_reservations = all_reservations.filter(content_type=rest_ct)

    context = {
        'hotel_reservations':       hotel_reservations,
        'restaurant_reservations':  restaurant_reservations,
        'reservation_count':        all_reservations.count(),
    }
    return render(request, 'panel/panel.html', context)


@login_required
def edit_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk, user=request.user)

    # تشخیص نوع شیء رزرو‌شده
    hotel_ct  = ContentType.objects.get_for_model(Hotel)
    rest_ct   = ContentType.objects.get_for_model(Restaurant)

    if res.content_type == hotel_ct:
        FormClass = HotelReservationForm
    else:                           # برای رستوران
        FormClass = RestaurantReservationForm

    if request.method == "POST":
        form = FormClass(request.POST, instance=res)
        if form.is_valid():
            form.save()
            return redirect("main:panel")
    else:
        form = FormClass(instance=res)

    return render(request, "panel/edit_reservation.html", {"form": form})


@login_required
@require_POST
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    reservation.delete()
    messages.success(request, 'رزرو با موفقیت حذف شد.')
    return redirect('main:panel')


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