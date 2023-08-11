from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser): ## add the user field that which admin is make the emp

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    password = models.CharField(_('password'), max_length=128)
    confirm_password = models.CharField(_('confirm password'), max_length=128)
    # Additional fields
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    
    # Department choices
    DEPARTMENT_CHOICES = [
        ('python', 'Python'),
        ('net', '.NET'),
        ('java', 'Java'),
        ('react', 'React'),
        ('angular', 'Angular'),
    ]
    department = models.CharField(_('department'), max_length=10, choices=DEPARTMENT_CHOICES)
    # Address fields
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=100)
    
    # State choices
    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh (Amaravati)'),
        ('Arunachal Pradesh', 'Arunachal Pradesh (Itanagar)'),
        ('Assam', 'Assam (Dispur)'),
        ('Bihar', 'Bihar (Patna)'),
        ('Chhattisgarh', 'Chhattisgarh (Raipur)'),
        ('Goa', 'Goa (Panaji)'),
        ('Gujarat', 'Gujarat (Gandhinagar)'),
        ('Haryana', 'Haryana (Chandigarh)'),
        ('Himachal Pradesh', 'Himachal Pradesh (Shimla)'),
        ('Jharkhand', 'Jharkhand (Ranchi)'),
        ('Karnataka', 'Karnataka (Bangalore)'),
        ('Kerala', 'Kerala (Thiruvananthapuram)'),
        ('Madhya Pradesh', 'Madhya Pradesh (Bhopal)'),
        ('Maharashtra', 'Maharashtra (Mumbai)'),
        ('Manipur', 'Manipur (Imphal)'),
        ('Meghalaya', 'Meghalaya (Shillong)'),
        ('Mizoram', 'Mizoram (Aizawl)'),
        ('Nagaland', 'Nagaland (Kohima)'),
        ('Odisha', 'Odisha (Bhubaneshwar)'),
        ('Punjab', 'Punjab (Chandigarh)'),
        ('Rajasthan', 'Rajasthan (Jaipur)'),
        ('Sikkim', 'Sikkim (Gangtok)'),
        ('Tamil Nadu', 'Tamil Nadu (Chennai)'),
        ('Telangana', 'Telangana (Hyderabad)'),
        ('Tripura', 'Tripura (Agartala)'),
        ('Uttarakhand', 'Uttarakhand (Dehradun)'),
        ('Uttar Pradesh', 'Uttar Pradesh (Lucknow)'),
        ('West Bengal', 'West Bengal (Kolkata)'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands (Port Blair)'),
        ('Chandigarh', 'Chandigarh (Chandigarh)'),
        ('Dadra and Nagar Haveli and Daman & Diu', 'Dadra and Nagar Haveli and Daman & Diu (Daman)'),
        ('The Government of NCT of Delhi', 'The Government of NCT of Delhi (Delhi)'),
        ('Jammu & Kashmir', 'Jammu & Kashmir (Srinagar-S*, Jammu-W*)'),
        ('Ladakh', 'Ladakh (Leh)'),
        ('Lakshadweep', 'Lakshadweep (Kavaratti)'),
        ('Puducherry', 'Puducherry (Puducherry)')
        # Add more choices as needed
    ]
    state = models.CharField(_('state'), max_length=40, choices=STATE_CHOICES)
    zipcode = models.CharField(_('zipcode'), max_length=10)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_CHOICES)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

