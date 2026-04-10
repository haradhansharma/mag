"""
Periodic Celery tasks for the MERIDIAN API.
"""

from datetime import datetime, timezone
from celery import shared_task

from users.models import AuthToken


@shared_task
def cleanup_expired_tokens():
    """Remove expired and orphaned authentication tokens."""
    now = datetime.now(timezone.utc)

    # Delete expired tokens
    expired_count = AuthToken.objects.filter(expires_at__lte=now).delete()[0]

    # Delete orphaned tokens (user has been deleted)
    orphaned_count = AuthToken.objects.filter(user__isnull=True).delete()[0]

    return {
        "expired_deleted": expired_count,
        "orphaned_deleted": orphaned_count,
    }
