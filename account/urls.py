# urls.py
from django.urls import path
from .views import UserRegistrationAPIView, LoginAPIView, UserListAPIView, LogoutView
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('resetpassword/',views.resetpassword,name='reset-password'),
    path('forgotpassword/',views.forgotpassword,name='forgot-password'),
    path('admin/',views.admin,name='admin'),
    path('home/',views.home,name='home'),





########### API ###########
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('get-users/', UserListAPIView.as_view(), name='user-list'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='logout'),
    
]
 