from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # صفحه اصلی و لیست‌ها
    path("", views.home, name="home"),
    path("hotels/", views.hotels, name="hotels"),
    path("restaurants/", views.restaurants, name="restaurants"),

    # جزئیات و رزرو
    path("hotels/<int:pk>/", views.hotel_detail, name="hotel_detail"),
    path("hotels/<int:pk>/reserve/", views.create_hotel_reservation, name="reserve_hotel"),

    path("restaurants/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurants/<int:pk>/reserve/", views.create_restaurant_reservation, name="reserve_restaurant"),

    # پنل کاربر
    path("panel/", views.panel, name="panel"),
    path("panel/reservation/<int:pk>/edit/", views.edit_reservation, name="reservation_edit"),
    path("panel/reservation/<int:pk>/delete/", views.delete_reservation, name="reservation_delete"),

    # احراز هویت
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    #دیدن جزئیات
    path("hotels/<int:pk>/", views.hotel_detail, name="hotel_detail"),
    path("restaurants/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),


]
