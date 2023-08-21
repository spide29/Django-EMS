from account.models import CustomAuditLog  # Import the CustomAuditLog model from the account app


def create_log_entry(user, action):
    CustomAuditLog.objects.create(user=user, action=action)
