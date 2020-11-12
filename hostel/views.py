from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, ListView, DetailView
from .models import Room_Type, Facility, Room, Payment, Student_In_Room, Reservation, Announcement
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import NewReservationForm
from django.http import JsonResponse
import requests
import json
from django.conf import settings
from decimal import Decimal
from django.db.models import F

# Create your views here.

#View for the Index Page
class IndexView(ListView):
    model = Room_Type
    context_object_name = 'room_types'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['facilities'] = Facility.objects.all()[:8]
        return context


class RoomsView(ListView):
    model = Room_Type
    context_object_name = 'room_types'
    template_name = 'rooms.html'


class AvailableRoomsView(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'rooms.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(AvailableRoomsView, self).get_context_data(**kwargs)
        context['room_type'] = self.room_type
        return context

    def get_queryset(self):
        self.room_type = get_object_or_404(Room_Type, pk=self.kwargs.get('room_type'))
        queryset = self.room_type.rooms.order_by('num_of_people')
        return queryset.filter(num_of_people__lt=self.room_type.capacity)

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'my_dashboard.html'
    paginate_by=4

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.order_by('-date_time') 
        return context

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user).order_by('-date')
        return queryset

@login_required
def check_room_availability(request, room):
    room = get_object_or_404(Room, pk=room)
    capacity = room.room_type.capacity
    if room.num_of_people < capacity:
        return JsonResponse({'status':'available'})
    else:
        return JsonResponse({'status':'unavailable'})


@login_required
def payment(request):
    reference = request.GET.get('response', None)
    reservation = request.GET.get('res', None)
    room = request.GET.get('room', None)

    headers = {
    'Authorization': settings.PAYSTACK_SECRET_KEY,
    }
    response = requests.get('https://api.paystack.co/transaction/verify/'+reference, headers=headers)
    x = response.json()

    success = x['data']['status']
    amount = x['data']['amount'] / 100

    if success == "success":
        room = Room.objects.get(pk=room)
        reservation = Reservation.objects.get(pk=reservation)

        post = Payment.objects.create(
            user = request.user,
            room = room,
            reservation = reservation,
            amount = amount
        )

        reservation.first_payment = "Paid"
        reservation.total_paid = F('total_paid') + amount
        reservation.save(update_fields=["total_paid", "first_payment"])

        ##Increment the number of people in the room 
        room.num_of_people += 1
        room.save()

        #add to student_in_room table
        student_in_room = Student_In_Room.objects.create(
            user = request.user,
            room = room,
            reservation = reservation
        )


    return JsonResponse(x, safe=False)



class AboutView(ListView):
    model = Facility
    context_object_name = 'facilities'
    template_name = 'about.html'

def contact(request):
    return render(request, 'contact.html')

def coming_soon(request):
    return render(request, 'coming_soon.html')


@login_required
def reserve_room(request, room_type, room):
    room = get_object_or_404(Room, room_type__pk=room_type, pk=room)
    is_available = room.room_type.capacity > room.num_of_people

    #check if room is available. if not, send an error message
    if not is_available:
        return render(request, 'reserve_room.html', {'room': room, 'errors':'Sorry! The room has been fully reserved! Kindly try another room'})

    #get last reservation
    #if not inform the user that he cannot reserve another room when he hasnt paid for the previous reservation
    last_reservation = Reservation.objects.filter(user=request.user).order_by('-date')[:1]
    if last_reservation:
        if last_reservation[0].total_amount > last_reservation[0].total_paid:
             return render(request, "reserve_room.html", {'errors':'Sorry! You cannot reserve another room while you have an incomplete reservation'})


    if request.method == 'POST':
        form = NewReservationForm(request.POST)
        if form.is_valid():
            #check if room is available again
            if is_available:
               

                reservation = form.save(commit=False)
                reservation.room = room
                reservation.user = request.user
                #reservation.arrival_date = form.cleaned_data.get('arrival_date')
                reservation.duration_type = form.cleaned_data.get('duration_type')
                reservation.duration = form.cleaned_data.get('duration')

                duration_type = form.cleaned_data.get('duration_type')
                duration = form.cleaned_data.get('duration')
                price_per_day = room.room_type.price_per_day
                price_per_week = room.room_type.price_per_week
                price_per_month = room.room_type.price_per_month
                price_per_sem = room.room_type.price_per_sem

                if duration_type == "Day":
                    reservation.total_amount = duration * price_per_day
                elif duration_type == "Week":
                    reservation.total_amount = duration * price_per_week
                elif duration_type == "Month":
                    reservation.total_amount = duration * price_per_month
                elif duration_type == "Sem":
                    reservation.total_amount = duration * price_per_sem

                reservation.save()


              
            else:
                return render(request, 'reserve_room.html', {'room': room, 'errors':'Sorry! The room has been fully reserved! Kindly try another room'})

            return redirect('dashboard')        

    else:
        form = NewReservationForm()
    return render(request, 'reserve_room.html', {'room': room, 'form': form})


@method_decorator(login_required, name='dispatch')
class PaymentsView(ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'payments.html'
    paginate_by = 7

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user).order_by('-date_time')
        return queryset

@login_required
def delete_reservation(request, reservation):
    reservation = get_object_or_404(Reservation, pk=reservation, user=request.user)
    reservation.delete()
    return redirect('dashboard') 
