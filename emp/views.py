from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import Employee
from .serializers import EmployeeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)  # Add this line to require authentication
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

