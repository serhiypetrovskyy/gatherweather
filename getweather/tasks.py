from django.core.mail import EmailMessage
from django.core import mail
from celery import shared_task


@shared_task()
def send_weather_report_email_task(email_data):
    email_list = []
    for email_dict in email_data:
        email = EmailMessage(
            subject=email_dict["subject"],
            body=email_dict["body"],
            to=email_dict["to"]
        )
        email.content_subtype = 'html'
        email_list.append(email)
    connection = mail.get_connection()
    connection.send_messages(email_list)
