from django.contrib import admin
from django.urls import path, include
from main import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotels/', views.hotels, name='hotels'),  # یا views.hotels_view اگر اسمش اون باشه
    path('', include('main.urls')),  # اگر اپ اصلی routeها رو اونجا داره
]
