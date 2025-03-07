from django.core.management.base import BaseCommand
from django.utils import timezone
from activities.models import Activity, ActivityLog
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Adds test logs to activity with ID 1'

    def handle(self, *args, **options):
        try:
            activity = Activity.objects.get(id=1)
            user = User.objects.first()  # Get the first user in the system
            
            dates = [
                "2025-02-20",
                "2025-02-18",
                "2025-02-21",
                "2025-02-27",
                "2025-03-03",
                "2025-03-05",
                "2025-03-05",
                "2025-03-06",
            ]

            for date_str in dates:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                ActivityLog.objects.create(
                    activity=activity,
                    user=user,
                    date=date,
                    notes=f"Test log for {date_str}"
                )
                self.stdout.write(self.style.SUCCESS(f'Created log for {date_str}'))

        except Activity.DoesNotExist:
            self.stdout.write(self.style.ERROR('Activity with ID 1 does not exist'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No users found in the system')) 