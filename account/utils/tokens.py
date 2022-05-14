from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_account_activation_token(user, subject, **kwargs):
    request = kwargs.get('request')
    current_site = get_current_site(request)
    message = render_to_string('auth/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        subject, message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.send()


def send_password_reset_token(user, subject, **kwargs):
    request = kwargs.get('request')
    current_site = get_current_site(request)
    message = render_to_string('auth/forgot-password/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        subject, message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.send()
