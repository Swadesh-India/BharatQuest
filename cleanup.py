from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()
cutoff_date = timezone.now() - timedelta(days=2)

stale_users = User.objects.filter(is_active=False, created_at__lte=cutoff_date)
count = stale_users.count()

if count > 0:
    stale_users.delete()
    print(f"Success: Deleted {count} unactivated account(s).")
else:
    print("Done: No unactivated accounts older than 2 days were found.")

