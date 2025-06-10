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


# @staff_member_required
# def admin_panel(request):
#     print("admin_panel view اجرا شد")
#     hotels = Hotel.objects.all()
#     restaurants = Restaurant.objects.all()
#     reservations = Reservation.objects.all()
#     return render(request, 'admin_panel.html', {
#         'hotels': Hotel,
#         'restaurants': Restaurant,
#         'reservations': Reservation,
#     })

# پنل اصلی
# @staff_member_required
# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')


# @staff_member_required
# def admin_dashboard(request):
#     context = {
#         'hotels': Hotel.objects.all(),
#         'restaurants': Restaurant.objects.all(),
#         'reservations': Reservation.objects.all(),
#         'users': User.objects.all()
#     }
#     return render(request, 'admin/dashboard.html', context)

# # --- هتل‌ها ---
# @staff_member_required
# def admin_hotels(request):
#     hotels = Hotel.objects.all()
#     return render(request, 'admin/hotels.html', {'hotels': hotels})

# @staff_member_required
# def add_hotel(request):
#     if request.method == 'POST':
#         Hotel.objects.create(
#             name=request.POST['name'],
#             location=request.POST['location'],
#             description=request.POST['description'],
#             price_per_night=request.POST['price_per_night'],
#             is_available=request.POST.get('is_available') == 'on',
#         )
#         return redirect('main:admin_hotels')
#     return render(request, 'admin/hotel_form.html')

# @staff_member_required
# def edit_hotel(request, hotel_id):
#     hotel = get_object_or_404(Hotel, id=hotel_id)
#     if request.method == 'POST':
#         hotel.name = request.POST['name']
#         hotel.location = request.POST['location']
#         hotel.description = request.POST['description']
#         hotel.price_per_night = request.POST['price_per_night']
#         hotel.is_available = request.POST.get('is_available') == 'on'
#         hotel.save()
#         return redirect('main:admin_hotels')
#     return render(request, 'admin/hotel_form.html', {'hotel': hotel})

# # --- رستوران‌ها ---
# @staff_member_required
# def admin_restaurants(request):
#     restaurants = Restaurant.objects.all()
#     return render(request, 'admin/restaurants.html', {'restaurants': restaurants})

# @staff_member_required
# def add_restaurant(request):
#     if request.method == 'POST':
#         Restaurant.objects.create(
#             name=request.POST['name'],
#             location=request.POST['location'],
#             description=request.POST['description'],
#             average_price=request.POST['average_price'],
#             is_available=request.POST.get('is_available') == 'on',
#         )
#         return redirect('main:admin_restaurants')
#     return render(request, 'admin/restaurant_form.html')

# @staff_member_required
# def edit_restaurant(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     if request.method == 'POST':
#         restaurant.name = request.POST['name']
#         restaurant.location = request.POST['location']
#         restaurant.description = request.POST['description']
#         restaurant.average_price = request.POST['average_price']
#         restaurant.is_available = request.POST.get('is_available') == 'on'
#         restaurant.save()
#         return redirect('main:admin_restaurants')
#     return render(request, 'admin/restaurant_form.html', {'restaurant': restaurant})

# # --- کاربران و رزروها ---
# @staff_member_required
# def admin_users(request):
#     users = User.objects.all()
#     return render(request, 'admin/users.html', {'users': users})

# @staff_member_required
# def admin_reservations(request):
#     reservations = Reservation.objects.all()
#     return render(request, 'admin/reservations.html', {'reservations': reservations})
