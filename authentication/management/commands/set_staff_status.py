from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Set the is_staff status for a specific user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('is_staff', type=bool, help='Staff status (True or False)')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        is_staff = kwargs['is_staff']

        try:
            user = User.objects.get(username=username)
            user.is_staff = is_staff
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated is_staff status for user {username} to {is_staff}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))

'''
use this to set a user as staff or not

python manage.py set_staff_status <username> <True|False>

for example,

python manage.py set_staff_status john_doe True
'''