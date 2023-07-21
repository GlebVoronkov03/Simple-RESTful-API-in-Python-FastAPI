import smtplib
from email.message import EmailMessage

from celery import Celery

from ..config import settings

celery = Celery(
    __name__,
    broker=f'{settings.redis_url}/0',
)


def get_email_template(sending_data: dict):
    email = EmailMessage()
    email['From'] = settings.smtp_user
    email['To'] = sending_data.get('email')
    email['Subject'] = sending_data.get('subject')
    email.set_content(
        sending_data.get('massage'),
        subtype='html'
    )
    return email


@celery.task
def send_email(sending_data: dict):
    email = get_email_template(sending_data)
    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(email)
