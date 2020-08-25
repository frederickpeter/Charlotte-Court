from django.test import TestCase
from django.urls import reverse
from .models import Room_Type, Facility

# Create your tests here.

#These are my helper methods
def create_room_type(capacity, price_per_sem):
    return Room_Type.objects.create(capacity=capacity, price_per_sem=price_per_sem)

def create_facility(name, icon):
    return Facility.objects.create(name=name, icon=icon)


class IndexViewTests(TestCase):
    def test_no_room_types(self):
        """
        if no room types exist an appropriate message is displayed
        """
        self.response = self.client.get(reverse('index'))
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, "No room types available")
        self.assertQuerysetEqual(self.response.context['room_types'], [])

    def test_no_facilities(self):
        """
        if no facilities exist an appropriate message is displayed
        """
        self.response = self.client.get(reverse('index'))
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, "No facilities available")
        self.assertQuerysetEqual(self.response.context['facilities'], [])

    def test_room_types(self):
        """
        if room types exist, they are returned
        """
        room_type1 = create_room_type(4, 4000)
        room_type2 = create_room_type(2, 4000)
        self.response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(self.response.context['room_types'], ['<Room_Type: 2 in a room>', '<Room_Type: 4 in a room>'])

    def test_facilities(self):
        """
        if facilities exist, they are returned
        """
        facilities1 = create_facility('facility1', 'fa fa-icon')
        facilities2 = create_facility('facility2', 'fa fa-icon')
        self.response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(self.response.context['facilities'], ['<Facility: facility1>', '<Facility: facility2>'])

    def test_max_8_facilities(self):
        """
        a max of 8 facilities will be shown
        """
        for i in range(10):
            create_facility('facility{}'.format(i), 'fa fa-icon')
        
        self.response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            self.response.context['facilities'], 
            ['<Facility: facility0>', '<Facility: facility1>',
            '<Facility: facility2>', '<Facility: facility3>',
            '<Facility: facility4>', '<Facility: facility5>',
            '<Facility: facility6>', '<Facility: facility7>']
        )


