# urls.py
from django.urls import path
from .views import UserRegistrationAPIView, LoginAPIView, UserListAPIView, LogoutView, UserTotalCountAPIView, UserListadminAPIView
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('addemp/',views.addemp,name='addemp'),
    path('resetpassword/',views.resetpassword,name='reset-password'),
    path('forgotpassword/',views.forgotpassword,name='forgot-password'),
    path('home/',views.home,name='home'),
    path('adminsite/',views.adminsite,name='adminsite'),
    path('adminleave/',views.adminleave,name='adminleave'),







########### API ###########
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('get-users/', UserListAPIView.as_view(), name='user-list'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='logout'),
    path('total-users/', UserTotalCountAPIView.as_view(), name='total-users'),
    path('user-list/', UserListadminAPIView.as_view(), name='user-list'),
    
]
 