from django.urls import path
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

#add namespace if you want, meaning to access these paths you have to do 'accounts:<url-name>'
app_name = 'accounts'
urlpatterns = [
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #because i use a namespace i had to put reverse url in some of the paths below. Remove them if you dont use namespace
    path('reset',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',email_template_name='accounts/password_reset_email.html',subject_template_name='accounts/password_reset_subject.txt', success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('myaccount/', account_views.UserUpdateView.as_view(), name='my_account'),
   
]

 
 