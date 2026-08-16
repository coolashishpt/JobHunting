from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_application_update_email(self, subject, body, from_email, recipient_list):
    """Send application update email (runs as a Celery task).

    from_email may be None; Django will use DEFAULT_FROM_EMAIL.
    recipient_list must be a list of emails.
    """
    try:
        send_mail(subject, body, from_email, recipient_list)
    except Exception:
        logger.exception('Failed to send application update email to %s', recipient_list)
        raise
