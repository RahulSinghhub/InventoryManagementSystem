import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(message, recipient="rrsmm152@gmail.com"):
    msg = MIMEMultipart()
    msg['From'] = "p1273105@gmail.com"
    msg['To'] = recipient
    msg['Subject'] = "Low Stock Alert"

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email@example.com", "your_password")
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
