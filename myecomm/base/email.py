from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

def send_account_email_activate(email, email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi, click on the link to activate your account http://127.0.0.1:8000/account/activate/{email_token}"
    send_mail(subject=subject, message=message, from_email=email_from, recipient_list=[email])