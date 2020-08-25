from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.admin.models import ADDITION, LogEntry

# Register your models here.
#admin.site.register(Facility)

#variables for the admin dashboard
admin.site.site_header = 'Charlotte Court Administration'
admin.site.site_title = 'Charlotte Admin'



# Unregister the provided model admin
admin.site.unregister(User)
# LogEntry.objects.filter(action_flag=ADDITION)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    search_fields = ("name__contains", )
    list_per_page = 10

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("date_time",)
    search_fields = ("title__contains", )
    list_per_page = 10

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "amount", "balance", "date_time")
    list_filter = ("date_time","room")
    search_fields = ("amount__contains","user__first_name__icontains","user__last_name__icontains", "room__name__contains")
    list_per_page = 10
    
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "room_type", "num_of_people")
    list_filter = ("room_type",)
    search_fields = ("name__contains",)
    list_per_page = 10


@admin.register(Student_In_Room)
class Student_In_Room_Admin(admin.ModelAdmin):
    list_display = ("user", "room")
    list_filter = ("room",)
    search_fields = ("user__first_name__icontains","user__last_name__icontains","room__name__contains")
    list_per_page = 10


@admin.register(Room_Type)
class Room_TypeAdmin(admin.ModelAdmin):
    list_display = ("room_type", "price_per_sem")
    search_fields = ("capacity__contains",)
    list_per_page = 10

    def room_type(self, obj):
        return '{} {}'.format(obj.capacity, 'in a room')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "duration_type", "duration", "date")
    list_filter = ("date","room",)
    search_fields = ("user__first_name__icontains", "user__last_name__icontains","room__name__contains")
    list_per_page = 10


# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    #prevent all users from being able to update the date joined and last_login field
    readonly_fields = [
        'date_joined', 'last_login', 'password'
    ]
    #controls what is displayed in the table
    list_display = ("first_name", "last_name", "username", "email", "is_staff")
    list_per_page = 10

    #prevent staff from updating the username of a user
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'is_staff',
                'user_permissions',
                'email',
                'is_active' 
                
            }

             # Prevent non-superusers from editing their own permissions
        # if (
        #     not is_superuser
        #     and obj is not None
        #     and obj == request.user
        # ):
            # disabled_fields |= {
                  
            # }


        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
            if f == 'email' and obj == request.user:
                form.base_fields[f].disabled=False
            if obj != None:
                if f == 'is_active' and  obj.is_superuser == False and obj.is_staff==False:
                    form.base_fields[f].disabled=False
                elif f == 'username' and  obj.is_superuser == False and obj.is_staff==False:
                    form.base_fields[f].disabled=False
            else:
                form.base_fields['username'].disabled=False

        return form