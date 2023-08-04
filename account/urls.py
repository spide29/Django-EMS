# urls.py
from django.urls import path
from .views import UserRegistrationAPIView, UserAuthenticationAPIView, UserListAPIView
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('resetpassword/',views.resetpassword,name='reset-password'),
    path('forgotpassword/',views.forgotpassword,name='forgot-password'),




########### API ###########
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('get-users/', UserListAPIView.as_view(), name='user-list'),
    path('login/', UserAuthenticationAPIView.as_view(), name='user-login'),
]
 