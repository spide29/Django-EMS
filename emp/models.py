from django.db import models
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _
from auditlog.models import AuditlogHistoryField

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

    history = AuditlogHistoryField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.from_date} to {self.to_date} ({self.status})'

class WorkAllocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_id = models.CharField(_('project ID'), max_length=20, unique=True)
    project_name = models.CharField(_('project name'), max_length=100)
    project_start_date = models.DateField(_('project start date'))
    project_end_date = models.DateField(_('project end date'))
    description = models.TextField(_('description'))
    leader_name = models.CharField(_('leader name'), max_length=50)
    client_name = models.CharField(_('client name'), max_length=100)
    # department = models.CharField(_('department'), max_length=50)
    technology = models.CharField(_('technology'), max_length=50)

    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.user.username} - {self.project_name}"

    def generate_project_id(self):
        last_project = WorkAllocation.objects.order_by('-id').first()
        if last_project:
            last_id = int(last_project.project_id.split('#')[1])
            new_id = last_id + 1
        else:
            new_id = 1
        return f"pro#{new_id:02}"

    def save(self, *args, **kwargs):
        if not self.project_id:
            self.project_id = self.generate_project_id()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('work allocation')
        verbose_name_plural = _('work allocations')


