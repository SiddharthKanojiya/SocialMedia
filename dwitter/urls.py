# dwitter/urls.py

from django.urls import path
from django.urls import reverse_lazy
from .views import dashboard, profile_list,profile,signup,userlogin,base,afterlogin_view,adddweet
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.views import ( 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from chatApp.views import chating


app_name = "dwitter"

urlpatterns = [
    path("", base, name="base"),
    path("dashboard", dashboard, name="dashboard"),
    path("afterlogin", afterlogin_view, name="afterlogin"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("signup",signup,name="signup"),
    path("userlogin",LoginView.as_view(template_name='dwitter/userlogin.html'),name="userlogin"),
    path("userlogout",LogoutView.as_view(template_name='base.html'),name="logout"),
    path('password_reset/', 
        PasswordResetView.as_view(
            template_name='dwitter/password_reset.html',
            html_email_template_name='dwitter/password_reset_email.html'
        ),
        
        name='password_reset'
    ),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='dwitter/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='dwitter/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name='dwitter/password_reset_complete.html'),name='password_reset_complete'),
    
    path('adddweet',adddweet,name="adddweet"),
    
    
    
]