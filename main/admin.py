from django.contrib import admin
from .models import Hotel, Restaurant, Reservation
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Hotel)
admin.site.register(Restaurant)
# admin.site.register(Reservation) #to add and change reservation

admin.site.unregister(Group) #so it won't show the group item
admin.site.unregister(User) #I'll customize it bellow:

#شخصی سازی پنل ادمین برای نمایش کاربران:
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

admin.site.register(User, CustomUserAdmin)    
