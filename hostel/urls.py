
from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomsView.as_view(), name="rooms"),
    path('rooms/<int:room_type>/', views.AvailableRoomsView.as_view(), name="available_rooms"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/<int:reservation>', views.DashboardView.as_view(), name='dashboard'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.contact, name='contact'),
    path('reservation/<int:room_type>/room/<int:room>/', views.reserve_room, name='reservation' ),
    path('reservation/<int:reservation>/delete/', views.delete_reservation, name='delete_reservation' ),
    path('dashboard/check-room-availability/<int:room>/', views.check_room_availability, name='check_room_availability'),
    path('verify_transaction', views.payment, name='payment'),
    path('payments', views.PaymentsView.as_view(), name='my-payments'),
    path('coming-soon/', views.coming_soon, name="coming_soon")
   
]
