from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from pysendpulse.pysendpulse import PySendPulse
from django.conf import settings
import logging

# Configure logging
# logging.basicConfig(filename='sendpulse_errors.log', level=logging.ERROR)


# Initialize SendPulse API client

def send_verification_email():
    # SendPulse API Credentials

    # api_id = settings.SENDPULSE_API_ID
    # api_secret = settings.SENDPULSE_API_SECRET
    # TOKEN_STORAGE = 'MEMCACHED'  # This file will store the OAuth token
    #
    # sendpulse = PySendPulse(api_id, api_secret, TOKEN_STORAGE)

    # Define sender and recipient
    # sender_email = settings.SENDPULSE_SENDER_EMAIL
    # recipient_email = 'ghalibhashimolanrewaju@unimaid.edu.ng'

    subject = 'Activate Your Account'
    # html_content = f"""
    #     <html>
    #     <body>
    #         <h2>Email Verification</h2>
    #         <p>Hi,</p>
    #         <p>Please verify your email by clicking the link below:</p>
    #         <p><a href="#">Verify your email</a></p>
    #         <p>If you did not create an account, please ignore this email.</p>
    #         <p>Best regards,<br>Your Company</p>
    #     </body>
    #     </html>
    #     """
    # message = render_to_string(html_content)
    msg = "Hello! How are you doing"
    send_mail(
        subject=subject,  # Subject
        message=msg, #strip_tags(message),  # message
        from_email=settings.EMAIL_HOST_USER,  # From Email
        recipient_list=["marufidrishormohumu@gmail.com"],  # To Email
        fail_silently=False
    )

    # response = sendpulse.smtp_send_mail(
    #     from_email=sender_email,
    #     to_email=recipient_email,
    #     subject=subject,
    #     html=html_content

    # Create email message
    # try:
    #     message = {
    #         'subject': subject,
    #         'html': html_content,
    #         'from': sender_email,
    #         'to': recipient_email
    #     }
    #
    #     # Send the email
    #     response = sendpulse.smtp_send_mail(message)
    #     return response
    # except Exception as e:
    #     logging.error(f"Error sending email: {e}")
    #     raise


# send_verification_email()


