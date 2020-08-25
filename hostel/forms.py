from django import forms
from .models import Reservation

#a form associated with the Topic model
class NewReservationForm(forms.ModelForm):
    # amount = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={'rows':5, 'placeholder': 'What is on your mind'}
    #     ), 
    #     max_length=4000,
    #     help_text='The max length of the text is 4000.'
    #     )

    class Meta:
        model = Reservation
        #subject is for the Topic class, message is for the Post class
        #these are the fields used to create the form 
        #since message is for Post we had to declare the widget above
        fields = ['duration_type', 'duration']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['message', ]