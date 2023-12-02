from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lt=month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()