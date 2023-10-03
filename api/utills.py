import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail

from file_shareing_system.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


class EmallManagement:
    def __init__(self, to_list = None, cc_list = None, request = None):
        self.to_list = to_list
        self.cc_list = cc_list
        self.request = request
        # self.password = kwargs.get('new_password')
    
    def register_user(self, password, username):
        # def weekly_save_notification_mail(subject,recipient_list,cc_email,html_message):
        subject = "Welcome to File Share System"
        html_message = "welcome_login.html"
        email_from = EMAIL_HOST_USER
        recipient_list = self.to_list
        
        html_message = render_to_string(html_message, {'password':password,'username':username})
        send_mail(subject, html_message, email_from, recipient_list, html_message=html_message)
    