# views.py
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer, UserListSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserAuthenticationSerializer
from datetime import timedelta
from django.shortcuts import render, redirect
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .models import CustomUser
from rest_framework import generics
CustomUser = get_user_model()



def signin(request):
    return render(request, 'account/signin.html')

def resetpassword(request):
    return render(request, 'account/reset.html')

def forgotpassword(request):
    return render(request, 'account/forgot.html')

def home(request):
    access_token = request.COOKIES.get('access_token')
    context = {
        'access_token': access_token,
    }
    return render(request, 'employee/emp_home.html', context)

# @user_passes_test(lambda user: user.is_superuser, login_url='admin:index')
def adminsite(request):
    access_token = request.COOKIES.get('access_token')
    context = {
        'access_token': access_token,
    }
    return render(request, 'account/home.html', context)

from .models import CustomUser

def addemp(request):
    options = CustomUser.DEPARTMENT_CHOICES
    state = CustomUser.STATE_CHOICES
    gender = CustomUser.GENDER_CHOICES
    return render(request, 'account/addemp.html', {'options': options,'state':state,'gender':gender})

def adminleave(request):
    access_token = request.COOKIES.get('access_token')
    context = {
        'access_token': access_token,
    }
    return render(request, 'account/adminleave.html', context)
# def home(request):
#   if request.user.is_authenticated:
#     return render(request, 'employee/emp_home.html')
#   else:
#     return redirect('login')
def workallocation(request):
    return render(request, 'account/workallocation.html')

########################################  API
class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        if len(phone_number) != 10:
            raise ValidationError({'phone_number': 'Mobile number must be 10 digits.'})
        username = serializer.validated_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({'username': 'This username is already in use.'})
        email = serializer.validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError({'email': 'This email address is already in use.'})
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        if password != confirm_password:
            raise ValidationError({'confirm_password': 'Passwords do not match.'})
        user = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
class UserDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class UserListadminAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=False)
    

from rest_framework.filters import BaseFilterBackend

class ExcludeSuperusersFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(is_superuser=True)

class UserListAPIView(ListAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated,)  # Make sure only authenticated users can access this view
    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

# class UserListAPIView(ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserRegistrationSerializer

# class UserAuthenticationAPIView(GenericAPIView):
#     serializer_class = UserAuthenticationSerializer
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             response_data = {
#                 'access_token': access_token,
#                 'user_id': user.id,
#                 'refresh': str(refresh),
#                 'username': user.username,
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginAPIView(CreateAPIView):
    serializer_class = UserAuthenticationSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User with this username does not exist')
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        if user.is_superuser:
            redirect_url = "/account/adminsite/"
        else:
            redirect_url = "/account/home/"
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response_data = {
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'redirect_url': redirect_url
        }
        response = Response(response_data)
        response.set_cookie(key='access_token', value=access_token, httponly=True, domain=None)

        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.data = {
            'message': 'success'
        }
        return response

class UserTotalCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total_users = CustomUser.objects.filter(is_superuser=False).count()
        return Response({"total_users": total_users}, status=status.HTTP_200_OK)