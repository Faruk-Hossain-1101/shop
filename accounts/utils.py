import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def genarate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))

    return otp

def send_code_to_user(email):
    subject = "One time password for email verification"
    otp_code = genarate_otp()
    user = User.objects.filter(email=email).first()
    current_site = settings.MY_SITE
    email_body = f"Hi {user.first_name} thanks for signing up on {current_site} please verify with one time password {otp_code} "
    from_email = settings.DEFAULT_FROM_EMAIL
    get_otp = OneTimePassword.objects.filter(user=user).first()
    if get_otp:
        get_otp.otp = otp_code
        get_otp.save()
    else: 
        OneTimePassword.objects.create(user=user, otp=otp_code)

    send_email =EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=True)







