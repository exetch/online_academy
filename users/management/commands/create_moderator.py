from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Create a specific superuser with email and password.'

    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            email='gassemark@gmail.com',
            email_verificated=True,
            first_name='moderator',
            last_name='moderatorov',
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        user.set_password('123qwe456rty')
        user.save()