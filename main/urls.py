from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Hotels section
    path('hotels/', views.hotels, name='hotels'),
    path('reserve/hotel/<int:hotel_id>/', views.reserve_hotel, name='reserve'),

    # Restaurants section
    path('restaurants/', views.restaurants, name='restaurants'),
    path('reserve/restaurant/<int:restaurant_id>/', views.reserve_restaurant, name='reserve_restaurant'),

    # User panel
    path('panel/', views.panel, name='panel'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
