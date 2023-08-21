# views.py
from email import message
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer, UserListSerializer, PasswordUpdateSerializer
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
from .utils import create_log_entry
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser


CustomUser = get_user_model()



def signin(request):
    return render(request, 'account/signin.html')

from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponse
def forgotpassword(request, uidb64, token):
    reset_user_pk = request.session.get('reset_user_pk')
    context = {
        'reset_user_pk': reset_user_pk,
        
    }
    return render(request, 'account/reset.html', context )


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def resetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(f"Received email: {email}")
        try:
            user = CustomUser.objects.get(email=email)
            print(f"Found user: {user}")
            token = default_token_generator.make_token(user)
            print(f"Found user: {user.pk}")
            request.session['reset_user_pk'] = user.pk
            uid_bytes = force_bytes(user.pk)
            token_encoded = force_bytes(token)
            uid = base64.urlsafe_b64encode(uid_bytes).decode()
            token_str = base64.urlsafe_b64encode(token_encoded).decode()
            current_site = get_current_site(request)
            reset_url = f'/account/forgotpassword/{uid}/{token_str}/'
            print(f"Reset URL: {reset_url}")
            reset_link = f'http://{current_site.domain}{reset_url}'
            subject = 'Password Reset'
            message = f'Click the following link to reset your password: {reset_link}'
            try:
                send_mail(subject, message, 'sender@example.com', [email], fail_silently=False)
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        except CustomUser.DoesNotExist:
            print("User not found.")
        except CustomUser.DoesNotExist:
            print("User not found.")
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
    access_token = request.COOKIES.get('access_token')
    context = {
        'access_token': access_token,
    }
    return render(request, 'account/workallocation.html', context)

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
        creating_user = request.user
        print("############################", creating_user)
        user = serializer.save()
        action = f"User {user.username} registered by {creating_user.username}"
        create_log_entry(user, action)  # Create a log entry for user registration
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
class PasswordUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    queryset = CustomUser.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('password')
            new_confirm_password = serializer.validated_data.get('confirm_password')
            if new_password and new_confirm_password and new_password == new_confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(id=user_id)
            action = f"User {user.username} deleted by {request.user.username}"
            create_log_entry(user, action)  # Create a log entry for user deletion
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

        action = f"User {user.username} logged in"
        create_log_entry(user, action) 
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
        # user = request.user  # Assuming the user is authenticated
        # if user:
        #     # Log the logout event
        #     action = f"User {user.username} logged out"
        #     create_log_entry(user, action)  # Create a log entry for user logout
        return response

class UserTotalCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total_users = CustomUser.objects.filter(is_superuser=False).count()
        return Response({"total_users": total_users}, status=status.HTTP_200_OK)