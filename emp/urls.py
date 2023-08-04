from django.urls import path
from .views import EmployeeCreateAPIView

app_name = 'emp'

urlpatterns = [
    # Other URL patterns
    path('create-employee/', EmployeeCreateAPIView.as_view(), name='create-employee'),
]
1