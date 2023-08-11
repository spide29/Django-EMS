from django.db import models
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accept', _('Accept')),
        ('cancel', _('Cancel')),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    from_date = models.DateField(_('from date'))
    to_date = models.DateField(_('to date'))
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(_('reason'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.from_date} to {self.to_date} ({self.status})'