from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15)
    date_of_birth = models.DateField(_('date of birth'),null= True, blank=True)
    password = models.CharField(_('password'), max_length=128)
    confirm_password = models.CharField(_('confirm password'), max_length=128)
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    # def clean(self):
    #     if self.password != self.confirm_password:
    #         raise ValidationError({"confirm_password": ["The passwords do not match."]})

    class Meta:
        swappable = 'AUTH_USER_MODEL'

