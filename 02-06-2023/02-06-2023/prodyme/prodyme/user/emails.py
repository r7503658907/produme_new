import random
import smtplib
from .models import prodymeUser

def send_otp_forgot_mail(email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('praveenrrc@gmail.com', "")
    subject = f'Your account Verification email'
    otp = random.randint(1000,9999)
    message = f'Your otp is {otp}'
    server.sendmail('praveenrrc@gmail.com', email, message)
    user_obj = prodymeUser.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
