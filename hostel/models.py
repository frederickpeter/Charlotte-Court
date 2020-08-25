from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User

def get_name(self):
    return '{} {}'.format(self.first_name, self.last_name)

User.add_to_class("__str__", get_name)

# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=100, help_text='Name must be a maximum of 100 characters', unique=True)
    icon = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return '%s' % (self.name)


class Room_Type(models.Model):
    capacity = models.PositiveSmallIntegerField()
    price_per_day = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    price_per_week = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    price_per_month = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    price_per_sem = models.DecimalField(max_digits=7, decimal_places=2)
    image1 = models.ImageField(null=True, blank=True, upload_to='static/images/', max_length=100)
    image2 = models.ImageField(null=True, blank=True, upload_to='static/images/', max_length=100)
    image3 = models.ImageField(null=True, blank=True, upload_to='static/images/', max_length=100)

    class Meta:
        ordering = ["capacity"]

    def __str__(self):
        return '{} {}'.format(self.capacity, 'in a room')

    def count_available_rooms(self):
        count = Room.objects.filter(room_type=self, num_of_people__lt=self.capacity).count()
        return count

class Room(models.Model):
    room_type = models.ForeignKey(Room_Type, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text='Name must be a maximum of 50 characters', unique=True)
    num_of_people = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=30, default='Available') #full or available

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    DURATION_TYPE = (
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
        ('Sem', 'Semester')
    )
    duration_type = models.CharField(max_length=5, choices=DURATION_TYPE)
    duration = models.PositiveSmallIntegerField(help_text='Example. 2 Semesters')

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return 'Room {} - {} {} - {}'.format(self.room.name, self.user.first_name, self.user.last_name, self.date)
       

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='payments', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name='payments', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_time"]


class Student_In_Room(models.Model):
    room = models.ForeignKey(Room, related_name='+', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name='+', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '{} - {}'.format(self.room.name, self.user)

    