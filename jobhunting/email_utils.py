import threading
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_email_async(subject, body, from_email, recipient_list):
    """Send email in a background thread. Non-blocking and logs failures.

    from_email: if falsy, settings.DEFAULT_FROM_EMAIL will be used.
    recipient_list: list of recipient emails.
    """
    if not recipient_list:
        return
    if not from_email:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

    def _send():
        try:
            send_mail(subject, body, from_email, recipient_list)
        except Exception:
            logger.exception("Failed to send email to %s", recipient_list)

    thread = threading.Thread(target=_send, daemon=True)
    thread.start()