from django.db import models
from account.models import CustomUser
class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='emp_info')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateField()
    # mobile_number = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    recent_project = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"