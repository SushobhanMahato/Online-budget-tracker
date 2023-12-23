
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_via_email(email, amount):

    # Gmail SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Gmail account credentials
    sender_email = 'mailto:tech.sitemaster@gmail.com'
    sender_password = 'gpktjvwseufxclqj'

    # Recipient email address
    recipient_email = 'mailto:' + email

    # Email content
    subject = 'Warning for extra money uses from budget tracker'
    message = f'You have crossed your saving goals limit for this month. You have spent a total of {amount} Rs. till now.'
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject


        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

    
        server.sendmail(sender_email, recipient_email, msg.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print(f'An error occurred while sending the email: {str(e)}')

    finally:
        server.quit()