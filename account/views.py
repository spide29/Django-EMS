# views.py
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserAuthenticationSerializer
from datetime import timedelta
from django.shortcuts import render, redirect
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
CustomUser = get_user_model()


def signup(request):
    return render(request, 'account/signup.html')

def signin(request):
    return render(request, 'account/signin.html')

def resetpassword(request):
    return render(request, 'account/reset.html')

def forgotpassword(request):
    return render(request, 'account/forgot.html')

def admin(request):
    return render(request, 'account/home.html')

def home(request):
    return render(request, 'employee/emp_home.html')

    
# def home(request):
#   if request.user.is_authenticated:
#     return render(request, 'employee/emp_home.html')
#   else:
#     return redirect('login')

########################################  API
class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
class UserListAPIView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

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
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response_data = {
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username,
        }
        response = Response(response_data)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        # Delete the access token cookie using the same key 'access_token'
        response.delete_cookie('access_token')
        response.data = {
            'message': 'success'
        }
        return response
